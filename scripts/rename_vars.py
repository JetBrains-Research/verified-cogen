# %%
import pathlib

import libcst as cst

# %%
import re

# %%
class RenameVariableTransformer(cst.CSTTransformer):
    def __init__(self):
        self.pattern = re.compile(r"d_\d+_(.+)_")

    def leave_Name(self, original_node: cst.Name, updated_node: cst.Name) -> cst.Name:
        match = self.pattern.match(original_node.value)
        if match:
            new_name = match.group(1)
            return updated_node.with_changes(value=new_name)
        return updated_node


bench = pathlib.Path("benches/HumanEval-Nagini/Bench")
for file in list(bench.glob("*.py")):
    with open(file, "r") as f:
        code = f.read()
    module = cst.parse_module(code)

    # Transform the CST
    transformer = RenameVariableTransformer()
    transformed_module = module.visit(transformer)

    # Convert the transformed CST back to source code
    transformed_code = transformed_module.code

    # Print the transformed code
    with open(file, "w") as f:
        f.write(transformed_code)
        print(f.name)
        print(file, transformed_code)
        f.close()