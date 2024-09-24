from verified_cogen.runners.parsers.parser import Parser
import json


class JsonParser(Parser):
    def __init__(self):
        super().__init__()

    def parse(self, text: str) -> str:
        return json.loads(text)["code"].replace("\\n", "\n")
