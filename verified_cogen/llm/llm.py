from typing import Optional

from grazie.api.client.chat.prompt import ChatPrompt
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.gateway import AuthType, GrazieApiGatewayClient
from grazie.api.client.llm_parameters import LLMParameters
from grazie.api.client.parameters import Parameters
from grazie.api.client.profiles import Profile
from verified_cogen.tools import extract_code_from_llm_output
import verified_cogen.llm.prompts as prompts


class LLM:
    def __init__(
        self,
        grazie_token: str,
        profile: str,
        prompt_dir: str,
        temperature: float,
        system_prompt: Optional[str] = None,
    ):
        self.grazie = GrazieApiGatewayClient(
            url=GrazieApiGatewayUrls.STAGING,
            grazie_jwt_token=grazie_token,
            auth_type=AuthType.USER,
        )
        self.profile = Profile.get_by_name(profile)
        self.prompt_dir = prompt_dir
        self.is_gpt = "gpt" in self.profile.name
        self.user_prompts = []
        self.responses = []
        self.had_errors = False
        self.temperature = temperature
        self.system_prompt = (
            system_prompt if system_prompt else prompts.sys_prompt(self.prompt_dir)
        )

    def _request(self, temperature: Optional[float] = None):
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

        return self.grazie.chat(
            chat=prompt,
            profile=self.profile,
            parameters={LLMParameters.Temperature: Parameters.FloatValue(temperature)},
        )

    def _make_request(self):
        response = self._request().content
        self.responses.append(response)
        return extract_code_from_llm_output(response)

    def produce(self, prg: str):
        self.user_prompts.append(
            prompts.produce_prompt(self.prompt_dir).format(program=prg)
        )
        return self._make_request()

    def add(self, prg: str, checks: str, function: Optional[str] = None):
        prompt = prompts.add_prompt(self.prompt_dir).format(program=prg, checks=checks)
        if "{function}" in prompt and function is not None:
            prompt = prompt.replace("{function}", function)
        self.user_prompts.append(prompt)
        return self._make_request()

    def rewrite(self, prg: str):
        self.user_prompts.append(
            prompts.rewrite_prompt(self.prompt_dir).replace("{program}", prg)
        )
        return self._make_request()

    def ask_for_fixed(self, err: str):
        prompt = (
            prompts.ask_for_fixed_had_errors_prompt(self.prompt_dir)
            if self.had_errors
            else prompts.ask_for_fixed_prompt(self.prompt_dir)
        )
        self.user_prompts.append(prompt.format(error=err))
        return self._make_request()

    def ask_for_timeout(self):
        self.user_prompts.append(prompts.ask_for_timeout_prompt(self.prompt_dir))
        return self._make_request()
