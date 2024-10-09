from verified_cogen.runners.languages.dafny import DafnyLanguage
from verified_cogen.runners.languages.language import AnnotationType, LanguageDatabase
from verified_cogen.runners.languages.nagini import NaginiLanguage
from verified_cogen.runners.languages.verus import VerusLanguage


def register_basic_languages(with_removed: list[AnnotationType]):
    LanguageDatabase().register("dafny", ["dfy"], DafnyLanguage(with_removed))
    LanguageDatabase().register("verus", ["rs"], VerusLanguage(with_removed))
    LanguageDatabase().register(
        "nagini", ["py", "python"], NaginiLanguage(with_removed)
    )
