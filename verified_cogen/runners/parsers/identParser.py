from verified_cogen.runners.parsers.parser import Parser


class IdentParser(Parser):
    def __init__(
        self,
    ):
        super().__init__()

    def parse(self, text: str) -> str:
        return text
