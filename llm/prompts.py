SYS_PROMPT = """
    You are an expert in a Rust verification framework Verus.
    You will be given tasks dealing with Rust programs and specifications.
    Do not provide ANY explanations. Don't include markdown backticks. Respond only in Rust code, nothing else.
    Take into account that arrays inside the invariants are indexed by type `int`.
"""

PRODUCE_INVARIANTS = """
    Given the following Rust program, output Verus invariants that should go into the `while` loop.
    Ensure that the invariants are as comprehensive as they can be.
    Even if you think some invariant is not totally necessary, better add it than not.
    The program:
    {program}
"""

REWRITE_WITH_INVARIANTS = """
    Rewrite the following Rust program, adding correct Verus invariants into `while` loops. 
    Do not change the code, only add the invariants.
    Ensure that the invariants are as comprehensive as they can be.
    Even if you think some invariant is not totally necessary, better add it than not.
    The program:
    {program}
"""

ADD_INVARIANTS = """
    Given the following Rust program, and a set of Verus invariants, output the program with invariants inserted into the correct place.
    The program:
    {program}
    –
    The invariants:
    {invariants}
"""

ASK_FOR_FIXED = """
    The following errors occurred during verification:
    {error}

    Please fix the error by adding, removing or modifying the invariants and return the fixed program.
"""

ASK_FOR_FIXED_HAD_ERRORS = """
    There are still some errors:
    {error}

    Could you please fix them?
"""
