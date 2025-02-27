from verified_cogen.runners.languages import AnnotationType

VALID_BENCH_TYPES = ["invariants", "generic", "generate", "validating", "step-by-step", "step-by-step-flusn"]

MODE_MAPPING = {
    "mode1": [AnnotationType.INVARIANTS, AnnotationType.ASSERTS],
    "mode2": [
        AnnotationType.INVARIANTS,
        AnnotationType.ASSERTS,
        AnnotationType.PRE_CONDITIONS,
        AnnotationType.POST_CONDITIONS,
    ],
    "mode3": [
        AnnotationType.INVARIANTS,
        AnnotationType.ASSERTS,
        AnnotationType.IMPLS,
    ],
    "mode4": [
        AnnotationType.INVARIANTS,
        AnnotationType.ASSERTS,
        AnnotationType.IMPLS,
    ],
    "mode5": [
        AnnotationType.INVARIANTS,
        AnnotationType.ASSERTS,
        AnnotationType.PRE_CONDITIONS,
        AnnotationType.POST_CONDITIONS,
        AnnotationType.IMPLS,
    ],
    "mode6": [
        AnnotationType.INVARIANTS,
        AnnotationType.ASSERTS,
        AnnotationType.PRE_CONDITIONS,
        AnnotationType.POST_CONDITIONS,
        AnnotationType.IMPLS,
        AnnotationType.PURE,
    ],
}

REMOVE_IMPLS_MAPPING = {
    "mode1": False,
    "mode2": False,
    "mode3": True,
    "mode4": True,
    "mode5": True,
    "mode6": True,
}

TEXT_DESCRIPTIONS = {
    "mode1": False,
    "mode2": False,
    "mode3": False,
    "mode4": True,
    "mode5": True,
    "mode6": True,
}
