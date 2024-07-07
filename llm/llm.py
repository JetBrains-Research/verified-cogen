import llm.prompts as prompts
from grazie.api.client.gateway import AuthType, GrazieApiGatewayClient, GrazieHeaders
from grazie.api.client.chat.prompt import ChatPrompt
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.profiles import Profile
from grazie.api.client.llm_parameters import LLMParameters
from grazie.api.client.parameters import Parameters
from modes import Modes
from utils import dafnybench_extract_code_from_llm_output


class LLM:

    def __init__(self, grazie_token, profile):
        self.grazie = GrazieApiGatewayClient(
            url=GrazieApiGatewayUrls.STAGING,
            grazie_jwt_token=grazie_token,
            auth_type=AuthType.USER
        )
        self.profile = Profile.get_by_name(profile)
        self.is_gpt = 'gpt' in self.profile.name

    def _request(self, prompt, temperature=0.3):
        if type(prompt) is str:
            prompt = ChatPrompt().add_system(prompts.SYS_PROMPT).add_user(prompt)
        return self.grazie.chat(
            chat=prompt,
            profile=self.profile,
            parameters={
                LLMParameters.Temperature: Parameters.FloatValue(temperature)
            }
        )

    def produce_invariants(self, prg):
        result = self._request(prompts.PRODUCE_INVARIANTS.format(program=prg)).content
        return dafnybench_extract_code_from_llm_output(result)

    def rewrite_with_invariants_llm_singlestep(self, prg):
        result = self._request(prompts.REWRITE_WITH_INVARIANTS.format(program=prg)).content
        return dafnybench_extract_code_from_llm_output(result)

    def rewrite_with_invariants_dafnybench(self, prg):
        result = self._request(
            ChatPrompt()
            .add_system(prompts.SYS_DAFNYBENCH_GPT if self.is_gpt else prompts.SYS_DAFNYBENCH_OTHER)
            .add_user(
                (prompts.REWRITE_WITH_INVARIANTS_DAFNYBENCH_GPT if self.is_gpt
                 else prompts.REWRITE_WITH_INVARIANTS_DAFNYBENCH_OTHER)
                + prg),
            temperature=0.3
        ).content
        return dafnybench_extract_code_from_llm_output(result)

    def rewrite_with_invariants(self, prg, *, mode):
        if mode == Modes.LLM_SINGLE_STEP:
            return self.rewrite_with_invariants_llm_singlestep(prg)
        elif mode == Modes.DAFNYBENCH:
            return self.rewrite_with_invariants_dafnybench(prg)
        else:
            assert False, f"Unexpected mode for program rewriting: {mode}"

    def add_invariants(self, prg, inv):
        result = self._request(prompts.ADD_INVARIANTS.format(program=prg, invariants=inv)).content
        return dafnybench_extract_code_from_llm_output(result)

