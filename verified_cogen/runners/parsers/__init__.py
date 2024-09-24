from verified_cogen.runners.parsers.identParser import IdentParser
from verified_cogen.runners.parsers.jsonParser import JsonParser
from verified_cogen.runners.parsers.parser import ParserDatabase


def register_basic_parsers():
    ParserDatabase().register("identParser", IdentParser())
    ParserDatabase().register("jsonParser", JsonParser())
