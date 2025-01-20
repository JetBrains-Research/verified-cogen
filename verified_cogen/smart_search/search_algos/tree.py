from __future__ import annotations

import copy
from logging import Logger
from pathlib import Path
from typing import List, Tuple, Optional

from verified_cogen.runners import Runner
from verified_cogen.tools.modes import Mode

node_count = 0


def get_node_counter() -> int:
    global node_count
    node_count += 1
    return node_count


class Tree:
    runner: Runner
    logger: Logger
    counter: int
    base_name: str
    code: str
    depth: int
    error: str
    children: List[Tree]

    def __init__(
        self,
        depth: int,
        code: str,
        error: str,
        counter: int,
        base_name: str,
        runner: Runner,
        logger: Logger,
    ):
        self.code = code
        self.depth = depth
        self.error = error
        self.counter = counter
        self.base_name = base_name
        self.runner = runner
        self.logger = logger
        self.children = []

    def generate_children(
        self,
        n: int,
        mode: Mode,
        text_description: Optional[str],
    ) -> Tuple[List[Tree], bool]:
        self.logger.info(f"Node {self.base_name}{self.counter} generates {n} children")
        while n > 0:
            new_counter = get_node_counter()
            self.logger.info(
                f"Node {self.base_name}{self.counter} generates a child {self.base_name}{new_counter}"
            )

            new_runner = copy.deepcopy(self.runner)
            new_runner.logger = self.runner.logger

            if self.depth == 0:
                inv_prg = new_runner.postprocess(
                    new_runner.invoke(self.code, mode, text_description)
                )
            else:
                if self.error == "Verification timed out":
                    inv_prg = new_runner.postprocess(new_runner.ask_for_timeout())
                else:
                    inv_prg = new_runner.postprocess(
                        new_runner.ask_for_fixed(self.error)
                    )

            verification_result = self.runner.verify_program(
                self.base_name, new_counter, inv_prg
            )

            if verification_result is None:
                self.logger.info("Verification timed out")
                self.children += [
                    Tree(
                        self.depth + 1,
                        inv_prg,
                        "Verification timed out",
                        new_counter,
                        self.base_name,
                        new_runner,
                        self.logger,
                    )
                ]
            else:
                verified_inv, out_inv, err_inv = verification_result
                if verified_inv:
                    self.logger.info("Verified")
                    self.children += [
                        Tree(
                            self.depth + 1,
                            inv_prg,
                            "",
                            new_counter,
                            self.base_name,
                            new_runner,
                            self.logger,
                        )
                    ]
                    return self.children, True

                self.logger.info("Verification failed:")
                self.logger.info(out_inv)
                self.logger.info(err_inv)

                new_error = out_inv + err_inv
                self.children += [
                    Tree(
                        self.depth + 1,
                        inv_prg,
                        new_error,
                        new_counter,
                        self.base_name,
                        new_runner,
                        self.logger,
                    )
                ]

            n -= 1
        return self.children, False

    def collect_edges(self) -> List[Tuple[int, int]]:
        result: List[Tuple[int, int]] = []
        for child in self.children:
            result += child.collect_edges()
            result.append((self.counter, child.counter))
        return result

    def dump_history(self, history_path: Path):
        name: str = self.base_name.split(".")[0]
        name += str(self.counter)
        self.runner.llm.dump_history(history_path / f"{name}.txt")
        for child in self.children:
            child.dump_history(history_path)
