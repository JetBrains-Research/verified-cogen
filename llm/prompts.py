SYS_PROMPT = """
    You are an expert in a Rust verification framework Verus.
    You will be given tasks dealing with Rust programs and specifications.
    Do not provide ANY explanations. Don't include markdown backticks. Respond only in Rust code, nothing else.
    Take into account that arrays inside the invariants are indexed by type `int`, so you cannot use `usize` or `u32` etc without casting.
    On the other hand, in the program itself you must use `usize`
"""

PRODUCE_INVARIANTS = """
    Given the following Rust program, output Verus invariants that should go into the `while` loop.
    Ensure that the invariants are as comprehensive as they can be.
    Even if you think some invariant is not totally necessary, better add it than not.
    Even if you think some invariant can be inferred from the preconditions, but still might be needed for the other invariants, add it.
    The program:
    {program}
"""

REWRITE_WITH_INVARIANTS = """
    Rewrite the following Rust program, adding correct Verus invariants into `while` loops. Do not change the code, only add invariants.
    Ensure that the invariants are as comprehensive as they can be.
    Even if you think some invariant is not totally necessary, better add it than not.
    Even if you think some invariant can be infered from the preconditions, but still might be needed for the other invariants, add it.
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
    The following error occurred during verification:
    {error}
    
    Please fix the error and return the fixed program.
"""