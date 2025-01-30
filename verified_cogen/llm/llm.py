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


class LLMGrazie(LLM):
    def __init__(
        self,
        grazie_token: str,
        profile: str,
        prompt_dir: str,
        temperature: float,
        system_prompt: Optional[str] = None,
    ):
        super().__init__(prompt_dir)
        self.grazie = GrazieApiGatewayClient(
            url=GrazieApiGatewayUrls.STAGING,
            grazie_jwt_token=grazie_token,
            auth_type=AuthType.USER,
        )
        self.profile = Profile.get_by_name(profile)
        self.prompt_dir = prompt_dir
        self.is_gpt = "gpt" in self.profile.name
        self.user_prompts: list[str] = []
        self.is_user_prompt_temporary: list[bool] = []
        self.responses: list[str] = []
        self.is_response_temporary: list[bool] = []
        self.had_errors = False
        self.temperature = temperature
        self.system_prompt = (
            system_prompt if system_prompt else prompts.sys_prompt(self.prompt_dir)
        )

    def add_user_prompt(self, prompt: str, temporary: bool = False):
        self.user_prompts.append(prompt)
        self.is_user_prompt_temporary.append(temporary)

    def add_response(self, response: str, temporary: bool = False):
        self.responses.append(response)
        self.is_response_temporary.append(temporary)

    def wipe_all(self):
        self.user_prompts = []
        self.is_user_prompt_temporary = []
        self.responses = []
        self.is_response_temporary = []

    def wipe_temporary(self):
        self.user_prompts = [
            prompt
            for prompt, temporary in zip(
                self.user_prompts, self.is_user_prompt_temporary
            )
            if not temporary
        ]
        self.responses = [
            response
            for response, temporary in zip(self.responses, self.is_response_temporary)
            if not temporary
        ]
        self.is_user_prompt_temporary = [False] * len(self.user_prompts)
        self.is_response_temporary = [False] * len(self.responses)

    def _request(
        self, temperature: Optional[float] = None, tries: int = 5
    ) -> ChatResponse:
        if tries == 0:
            raise Exception("Exhausted tries to get response from Grazie API")
        if temperature is None:
            temperature = self.temperature
        prompt = ChatPrompt().add_system(self.system_prompt)
        current_prompt_user = 0
        current_response = 0
        while current_prompt_user < len(self.user_prompts) or current_response < len(
            self.responses
        ):
            if current_prompt_user < len(self.user_prompts):
                prompt = prompt.add_user(self.user_prompts[current_prompt_user])
                current_prompt_user += 1
            if current_response < len(self.responses):
                prompt = prompt.add_assistant(self.responses[current_response])
                current_response += 1

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
        prompt = (
            prompts.ask_for_fixed_had_errors_prompt(self.prompt_dir)
            if self.had_errors
            else prompts.ask_for_fixed_prompt(self.prompt_dir)
        )
        self.add_user_prompt(prompt.format(error=err))
        return self.make_request()

    def ask_for_timeout(self) -> str:
        self.add_user_prompt(prompts.ask_for_timeout_prompt(self.prompt_dir))
        return self.make_request()

    def dump_history(self, file: Path):
        with open(file, "w") as f:
            current_prompt_user = 0
            current_response = 0
            while current_prompt_user < len(
                self.user_prompts
            ) or current_response < len(self.responses):
                if current_prompt_user < len(self.user_prompts):
                    user_prompt = self.user_prompts[current_prompt_user]
                    f.write(f"User: {user_prompt}\n\n")
                    current_prompt_user += 1
                if current_response < len(self.responses):
                    f.write(f"LLM: {self.responses[current_response]}\n\n")
                    current_response += 1


class LLMOllama(LLM):
    def __init__(self, model: str, prompt_dir: str, temperature: float = 0.7):
        super().__init__(prompt_dir)
        self.model = model
        self.prompt_dir = prompt_dir
        self.temperature = temperature
        self.messages: list[dict[str, str]] = []
        self.message_is_temporary: list[bool] = []
        self.system_prompt = prompts.sys_prompt(self.prompt_dir)
        self._add_system_message(self.system_prompt)

    def _add_system_message(self, content: str):
        self.messages.append({"role": "system", "content": content})
        self.message_is_temporary.append(False)

    def add_user_prompt(self, prompt: str, temporary: bool = False):
        self.messages.append({"role": "user", "content": prompt})
        self.message_is_temporary.append(temporary)

    def add_response(self, response: str, temporary: bool = False):
        self.messages.append({"role": "assistant", "content": response})
        self.message_is_temporary.append(temporary)

    def wipe_all(self) -> None:
        self.messages = []
        self.message_is_temporary = []

    def wipe_temporary(self) -> None:
        self.messages = [
            m for m, t in zip(self.messages, self.message_is_temporary) if not t
        ]
        self.message_is_temporary = [False] * len(self.messages)

    def make_request(self) -> str:
        response = ollama.chat(model=self.model, messages=self.messages)  # type: ignore
        assert isinstance(response, ollama.ChatResponse)
        content = response["message"]["content"]
        self.add_response(content)
        return extract_code_from_llm_output(content)

    def produce(self, prg: str) -> str:
        prompt = prompts.produce_prompt(self.prompt_dir).format(program=prg)
        self.add_user_prompt(prompt)
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
        self.add_response(result)
        return self.make_request()

    def ask_for_fixed(self, err: str) -> str:
        prompt = prompts.ask_for_fixed_prompt(self.prompt_dir).format(error=err)
        self.add_user_prompt(prompt)
        return self.make_request()

    def ask_for_timeout(self) -> str:
        prompt = prompts.ask_for_timeout_prompt(self.prompt_dir)
        self.add_user_prompt(prompt)
        return self.make_request()

    def dump_history(self, file: Path):
        with open(file, "w") as f:
            for message in self.messages:
                role = message["role"].capitalize()
                content = message["content"]
                f.write(f"{role}: {content}\n\n")
