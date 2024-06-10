

SYS_PROMPT = """
    You are an expert in Dafny. 
    You will be given tasks dealing with Dafny programs including precise docstrings and specifications. 
    Do not provide explanations. Do not repeat given programs, answer with new content only.
    Respond only in dafny code.
"""

PRODUCE_INVARIANTS = """
    Given the following dafny program, output invariants that should go into the `while` loop:
    {program}
"""