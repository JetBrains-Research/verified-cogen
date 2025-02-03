import logging
from abc import ABC, abstractmethod
from http.client import RemoteDisconnected
from pathlib import Path
from typing import Optional

import ollama
from grazie.api.client.chat.prompt import ChatPrompt
from grazie.api.client.chat.response import ChatResponse
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.gateway import (
    AuthType,
    GrazieApiGatewayClient,
    RequestFailedException,
)
from grazie.api.client.llm_parameters import LLMParameters
from grazie.api.client.parameters import Parameters
from grazie.api.client.profiles import Profile

import verified_cogen.llm.prompts as prompts
from verified_cogen.tools import extract_code_from_llm_output

logger = logging.getLogger(__name__)


class LLM(ABC):
    prompt_dir: str

    def __init__(self, prompt_dir: str):
        self.prompt_dir = prompt_dir

    @abstractmethod
    def add_user_prompt(self, prompt: str, temporary: bool = False) -> None: ...

    @abstractmethod
    def add_response(self, response: str, temporary: bool = False) -> None: ...

    @abstractmethod
    def make_request(self) -> str: ...

    @abstractmethod
    def produce(self, prg: str) -> str: ...

    @abstractmethod
    def add(self, prg: str, checks: str, function: Optional[str] = None) -> str: ...

    @abstractmethod
    def rewrite(
        self,
        prg: str,
        text_description: Optional[str] = None,
        additional_prompt: str = "",
    ) -> str: ...

    @abstractmethod
    def ask_for_fixed(self, err: str) -> str: ...

    @abstractmethod
    def ask_for_timeout(self) -> str: ...

    @abstractmethod
    def dump_history(self, file: Path) -> None: ...

    @abstractmethod
    def wipe_all(self) -> None: ...

    @abstractmethod
    def wipe_temporary(self) -> None: ...


class LLMGeneric(LLM):
    def __init__(
        self, prompt_dir: str, temperature: float, system_prompt: Optional[str] = None
    ):
        super().__init__(prompt_dir)
        self.prompt_dir = prompt_dir
        self.temperature = temperature
        self.system_prompt = (
            system_prompt if system_prompt else prompts.sys_prompt(self.prompt_dir)
        )
        self.messages: list[dict[str, str]] = []
        self.message_is_temporary: list[bool] = []

    def add_user_prompt(self, prompt: str, temporary: bool = False):
        self.messages.append({"role": "user", "content": prompt})
        self.message_is_temporary.append(temporary)

    def add_response(self, response: str, temporary: bool = False):
        self.messages.append({"role": "assistant", "content": response})
        self.message_is_temporary.append(temporary)

    def wipe_all(self):
        self.messages = []
        self.message_is_temporary = []

    def wipe_temporary(self):
        self.messages = [
            m for m, t in zip(self.messages, self.message_is_temporary) if not t
        ]
        self.message_is_temporary = [False] * len(self.messages)

    @abstractmethod
    def make_request(self) -> str: ...

    def produce(self, prg: str) -> str:
        self.add_user_prompt(
            prompts.produce_prompt(self.prompt_dir).format(program=prg)
        )
        return self.make_request()

    def add(self, prg: str, checks: str, function: Optional[str] = None) -> str:
        prompt = prompts.add_prompt(self.prompt_dir).format(program=prg, checks=checks)
        if "{function}" in prompt and function is not None:
            prompt = prompt.replace("{function}", function)
        self.add_user_prompt(prompt)
        return self.make_request()

    def rewrite(
        self,
        prg: str,
        text_description: Optional[str] = None,
        additional_prompt: str = "",
    ) -> str:
        result = prompts.rewrite_prompt(self.prompt_dir).replace("{program}", prg)
        if text_description is not None and "{text_description}" in result:
            result = result.replace("{text_description}", text_description)
        result = result + "\n" + additional_prompt
        self.add_user_prompt(result)
        return self.make_request()

    def ask_for_fixed(self, err: str) -> str:
        prompt = prompts.ask_for_fixed_prompt(self.prompt_dir).format(error=err)
        self.add_user_prompt(prompt)
        return self.make_request()

    def ask_for_timeout(self) -> str:
        self.add_user_prompt(prompts.ask_for_timeout_prompt(self.prompt_dir))
        return self.make_request()

    def dump_history(self, file: Path):
        with open(file, "w") as f:
            for message in self.messages:
                role = message["role"].capitalize()
                content = message["content"]
                f.write(f"{role}: {content}\n\n")


class LLMGrazie(LLMGeneric):
    def __init__(
        self,
        grazie_token: str,
        profile: str,
        prompt_dir: str,
        temperature: float,
        system_prompt: Optional[str] = None,
    ):
        super().__init__(prompt_dir, temperature, system_prompt)
        self.grazie = GrazieApiGatewayClient(
            url=GrazieApiGatewayUrls.STAGING,
            grazie_jwt_token=grazie_token,
            auth_type=AuthType.USER,
        )
        self.profile = Profile.get_by_name(profile)
        self.is_gpt = "gpt" in self.profile.name
        self.had_errors = False
        self.messages.append({"role": "system", "content": self.system_prompt})
        self.message_is_temporary.append(False)

    def _request(
        self, temperature: Optional[float] = None, tries: int = 5
    ) -> ChatResponse:
        if tries == 0:
            raise Exception("Exhausted tries to get response from Grazie API")
        if temperature is None:
            temperature = self.temperature

        prompt = ChatPrompt()
        for message in self.messages:
            match message["role"]:
                case "system":
                    prompt = prompt.add_system(message["content"])
                case "user":
                    prompt = prompt.add_user(message["content"])
                case "assistant":
                    prompt = prompt.add_assistant(message["content"])
                case _:
                    raise ValueError(f"Unknown role: {message['role']}")

        try:
            return self.grazie.chat(
                chat=prompt,
                profile=self.profile,
                parameters={
                    LLMParameters.Temperature: Parameters.FloatValue(temperature)
                },
            )
        except (RemoteDisconnected, RequestFailedException):
            logger.warning("Grazie API is down, retrying...")
            return self._request(temperature, tries - 1)
        except Exception as e:
            self.dump_history(Path("err_dump.txt"))
            raise e

    def make_request(self) -> str:
        response = self._request().content
        self.add_response(response)
        return extract_code_from_llm_output(response)


class LLMOllama(LLMGeneric):
    def __init__(self, model: str, prompt_dir: str, temperature: float = 0.7):
        super().__init__(prompt_dir, temperature)
        self.model = model
        self.messages.append({"role": "system", "content": self.system_prompt})
        self.message_is_temporary.append(False)

    def make_request(self) -> str:
        response = ollama.chat(  # type: ignore
            model=self.model,
            messages=self.messages,
            options={"temperature": self.temperature},
        )
        assert isinstance(response, ollama.ChatResponse)
        content = response["message"]["content"]
        self.add_response(content)
        return extract_code_from_llm_output(content)
