from logging import Logger
from typing import Tuple

from verified_cogen.runners import Runner
from verified_cogen.smart_search.search_algos.tree import Tree
from verified_cogen.tools.modes import Mode


class SearchAlgo:
    tree: Tree
    breadth: int
    depth: int
    runner: Runner
    logger: Logger

    def __init__(self, breadth: int, depth: int, runner: Runner, mode: Mode):
        self.logger = runner.logger
        self.runner = runner
        self.depth = depth
        self.breadth = breadth
        self.mode = mode

    def run_on_file(self, file: str) -> Tuple[int, int]: ...
