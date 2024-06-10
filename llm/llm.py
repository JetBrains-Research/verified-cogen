import llm.prompts as prompts
from grazie.api.client.gateway import AuthType, GrazieApiGatewayClient, GrazieHeaders
from grazie.api.client.chat.prompt import ChatPrompt
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.profiles import Profile


class LLM:

    def __init__(self, grazie_token):
        self.grazie = GrazieApiGatewayClient(
            url=GrazieApiGatewayUrls.STAGING,
            grazie_jwt_token=grazie_token,
            auth_type=AuthType.USER
        )

    def _request(self, prompt):
        if type(prompt) is str:
            prompt = ChatPrompt().add_system(prompts.SYS_PROMPT).add_user(prompt)
        return self.grazie.chat(
            chat=prompt,
            profile=Profile.OPENAI_GPT_4
        )

    def produce_invariants(self, prg):
        return self._request(prompts.PRODUCE_INVARIANTS.format(program=prg))
