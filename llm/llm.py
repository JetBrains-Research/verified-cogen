import llm.prompts as prompts
from grazie.api.client.gateway import AuthType, GrazieApiGatewayClient, GrazieHeaders
from grazie.api.client.chat.prompt import ChatPrompt
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.profiles import Profile
from grazie.api.client.llm_parameters import LLMParameters
from grazie.api.client.parameters import Parameters
from modes import Modes


class LLM:
    def __init__(self, grazie_token, profile):
        self.grazie = GrazieApiGatewayClient(
            url=GrazieApiGatewayUrls.STAGING,
            grazie_jwt_token=grazie_token,
            auth_type=AuthType.USER,
        )
        self.profile = Profile.get_by_name(profile)
        self.is_gpt = "gpt" in self.profile.name
        self.user_prompts = []
        self.responses = []

    def _request(self, temperature=0.3):
        prompt = ChatPrompt().add_system(prompts.SYS_PROMPT)
        current_prompt_user = 0
        current_response = 0
        while current_prompt_user < len(self.user_prompts) or current_response < len(self.responses):
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

    def rewrite_with_invariants_llm_singlestep(self, prg):
        self.user_prompts.append(prompts.REWRITE_WITH_INVARIANTS.format(program=prg))
        return self._make_request()

    def rewrite_with_invariants(self, prg, *, mode):
        if mode == Modes.LLM_SINGLE_STEP:
            return self.rewrite_with_invariants_llm_singlestep(prg)
        else:
            assert False, f"Unexpected mode for program rewriting: {mode}"

    def ask_for_fixed(self, err):
        self.user_prompts.append(prompts.ASK_FOR_FIXED.format(error=err))
        return self._make_request()

    def add_invariants(self, prg, inv):
        self.user_prompts.append(prompts.ADD_INVARIANTS.format(program=prg, invariants=inv))
        return self._make_request()
