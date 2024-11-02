import ast
from _ast import Compare, expr
from typing import List


class InequalityReplacer(ast.NodeTransformer):
    def visit_Compare(self, node: Compare):
        if len(node.comparators) > 1:
            new_nodes: List[expr] = []
            left: expr = node.left
            left = self.visit(left)
            for op, right in zip(node.ops, node.comparators):
                right = self.visit(right)
                new_nodes.append(ast.Compare(left=left, ops=[op], comparators=[right]))
                left = right
            return ast.BoolOp(op=ast.And(), values=new_nodes)
        self.generic_visit(node)
        return node


def replace_inequalities(code: str) -> str:
    tree = ast.parse(code)

    transformer = InequalityReplacer()
    modified_tree = transformer.visit(tree)

    ast.fix_missing_locations(modified_tree)

    new_code = ast.unparse(modified_tree)
    return new_code


class DoubleInequalityChecker(ast.NodeVisitor):
    def __init__(self):
        self.has_double_inequality: bool = False

    def visit_Compare(self, node: Compare):
        if len(node.comparators) > 1:
            self.has_double_inequality = True
        self.generic_visit(node)


def contains_double_inequality(code: str) -> bool:
    tree = ast.parse(code)

    checker = DoubleInequalityChecker()
    checker.visit(tree)
    return checker.has_double_inequality
