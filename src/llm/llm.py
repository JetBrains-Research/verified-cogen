import llm.prompts as prompts
from grazie.api.client.gateway import AuthType, GrazieApiGatewayClient, GrazieHeaders
from grazie.api.client.chat.prompt import ChatPrompt
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.profiles import Profile
from grazie.api.client.llm_parameters import LLMParameters
from grazie.api.client.parameters import Parameters
from modes import Mode


class LLM:
    def __init__(self, grazie_token, profile, temperature):
        self.grazie = GrazieApiGatewayClient(
            url=GrazieApiGatewayUrls.STAGING,
            grazie_jwt_token=grazie_token,
            auth_type=AuthType.USER,
        )
        self.profile = Profile.get_by_name(profile)
        self.is_gpt = "gpt" in self.profile.name
        self.user_prompts = []
        self.responses = []
        self.had_errors = False
        self.temperature = temperature

    def _request(self, temperature=None):
        if temperature is None:
            temperature = self.temperature
        prompt = ChatPrompt().add_system(prompts.SYS_PROMPT)
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
        return response

    def produce_invariants(self, prg):
        self.user_prompts.append(prompts.PRODUCE_INVARIANTS.format(program=prg))
        return self._make_request()

    def produce_preconditions(self, prg):
        self.user_prompts.append(prompts.PRODUCE_PRECONDITIONS.format(program=prg))
        return self._make_request()

    def rewrite_with_invariants(self, prg):
        self.user_prompts.append(prompts.REWRITE_WITH_INVARIANTS.format(program=prg))
        return self._make_request()

    def rewrite_with_preconditions(self, prg):
        self.user_prompts.append(prompts.REWRITE_WITH_PRECONDITIONS.format(program=prg))
        return self._make_request()

    def ask_for_fixed_invariants(self, err):
        prompt = (
            prompts.ASK_FOR_FIXED_HAD_ERRORS
            if self.had_errors
            else prompts.ASK_FOR_FIXED_INVARIANTS
        )
        self.user_prompts.append(prompt.format(error=err))
        return self._make_request()

    def ask_for_fixed_preconditions(self, err):
        prompt = (
            prompts.ASK_FOR_FIXED_HAD_ERRORS
            if self.had_errors
            else prompts.ASK_FOR_FIXED_PRECONDITIONS
        )
        self.user_prompts.append(prompt.format(error=err))
        return self._make_request()

    def add_invariants(self, prg, inv):
        self.user_prompts.append(
            prompts.ADD_INVARIANTS.format(program=prg, invariants=inv)
        )
        return self._make_request()

    def add_preconditions(self, prg, pre):
        self.user_prompts.append(
            prompts.ADD_PRECONDITIONS.format(program=prg, preconditions=pre)
        )
        return self._make_request()
