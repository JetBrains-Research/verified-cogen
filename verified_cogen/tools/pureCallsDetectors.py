import ast
from typing import cast


class PureFunctionCallReplacer(ast.NodeTransformer):
    def __init__(self, pure_non_helpers: list[str]):
        self.pure_functions: list[str] = list()
        self.detected_calls: list[str] = list()
        self.current_function = None
        self.in_pure_function = False
        self.in_condition = False
        self.pure_non_helpers = pure_non_helpers

    def visit_FunctionDef(self, node: ast.FunctionDef):
        is_pure = any(isinstance(decorator, ast.Name) and decorator.id == "Pure" for decorator in node.decorator_list)
        if is_pure and node.name not in self.pure_non_helpers:
            self.pure_functions.append(node.name)

        prev_function = self.current_function
        prev_in_pure = self.in_pure_function
        self.current_function = node.name
        self.in_pure_function = is_pure

        if not is_pure:
            self.generic_visit(node)

        self.current_function = prev_function
        self.in_pure_function = prev_in_pure
        return node

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            if (
                node.func.id in self.pure_functions
                and not self.in_pure_function
                and not self.in_condition
                and self.current_function is not None
            ):
                self.detected_calls.append(node.func.id)
                return ast.Call(
                    func=ast.Name(id="invalid_call", ctx=ast.Load()),
                    args=[],
                    keywords=[],
                )
            if node.func.id not in ["Invariant", "Assert", "Requires", "Ensures"]:
                return self.generic_visit(node)
        return node

    def visit_If(self, node: ast.If):
        prev_in_condition = self.in_condition
        self.in_condition = True
        node.test = self.visit(node.test)
        self.in_condition = prev_in_condition
        node.body = [self.visit(stmt) for stmt in node.body]
        node.orelse = [self.visit(stmt) for stmt in node.orelse]
        return node

    def visit_While(self, node: ast.While):
        prev_in_condition = self.in_condition
        self.in_condition = True
        node.test = self.visit(node.test)
        self.in_condition = prev_in_condition
        node.body = [self.visit(stmt) for stmt in node.body]
        return node

    def visit_Assert(self, node: ast.Assert):
        prev_in_condition = self.in_condition
        self.in_condition = True
        node = cast(ast.Assert, self.generic_visit(node))
        self.in_condition = prev_in_condition
        return node


def detect_and_replace_pure_calls_nagini(code: str, pure_non_helpers: list[str]) -> tuple[list[str], str]:
    tree = ast.parse(code)
    replacer = PureFunctionCallReplacer(pure_non_helpers)
    modified_tree = replacer.visit(tree)
    new_code = ast.unparse(modified_tree)
    return replacer.detected_calls, new_code
