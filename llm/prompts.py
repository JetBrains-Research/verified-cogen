

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

REWRITE_WITH_INVARIANTS = """
    Rewrite the following dafny program, adding correct invariants into `while` loops. Do not change the code, only add invariants.
    The program:
    {program}
"""

ADD_INVARIANTS = """
    Given the following danfy program, and a set of invariants, output the program with invariants inserted into the correct place.
    The program:
    {program}
    –
    The invariants:
    {invariants}
"""

SYS_DAFNYBENCH_GPT = "You are an expert in Dafny. \
You will be given tasks dealing with Dafny programs including precise annotations.\n"

REWRITE_WITH_INVARIANTS_DAFNYBENCH_GPT = "Given a Dafny program with function signature, preconditions, postconditions, and code, but with annotations missing. \
Please return a complete Dafny program with the strongest possible annotations (loop invariants, assert statements, etc.) filled back in. \
Do not explain. \
Please use exactly the same function signature, preconditions, and postconditions. Do not ever modify the given lines. \
Below is the program:\n"

SYS_DAFNYBENCH_OTHER = "You are an expert in Dafny. \
You will be given tasks dealing with Dafny programs including precise annotations. \
You should only return code body in all circumstances. No text is allowed.\n"

REWRITE_WITH_INVARIANTS_DAFNYBENCH_OTHER = "Given a Dafny program with function signature, preconditions, postconditions, and code, but with annotations missing. \
Please return a complete Dafny program with the strongest possible annotation (loop invariants, assert statements, etc.) filled back in. \
Do not explain or output any text. If you have to explain, put all explanations in comments form. \
There should only be code body in your output. \
Please use exactly the same function signature, preconditions, and postconditions. Do not ever modify the given lines. \
Below is the program:\n```dafny\n"