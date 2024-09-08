from verified_cogen.runners.languages.dafny import DafnyLanguage
from verified_cogen.runners.languages.language import LanguageDatabase
from verified_cogen.runners.languages.nagini import NaginiLanguage


def init_basic_languages():
    LanguageDatabase().add("dafny", ["dfy"], DafnyLanguage())
    LanguageDatabase().add("nagini", ["py", "python"], NaginiLanguage())
