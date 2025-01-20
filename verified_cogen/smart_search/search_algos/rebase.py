from pathlib import Path
from typing import Tuple, List

from verified_cogen.runners import Runner
from verified_cogen.smart_search.scoring_functions import ScoringFunction
from verified_cogen.smart_search.search_algos import SearchAlgo
from verified_cogen.smart_search.search_algos.tree import Tree, get_node_counter
from verified_cogen.tools import basename
from verified_cogen.tools.modes import Mode


class Rebase(SearchAlgo):
    scoring_function: ScoringFunction

    def __init__(
        self,
        breadth: int,
        depth: int,
        runner: Runner,
        mode: Mode,
        scoring_function: ScoringFunction,
    ):
        super().__init__(breadth, depth, runner, mode)
        self.scoring_function = scoring_function

    def gen_scores(self, vertices: List[Tree]) -> List[int]:
        scores: List[float] = [
            self.scoring_function.score(node.code, node.error) for node in vertices
        ]

        import math

        max_score: float = max(scores)
        scores = [math.exp(x - max_score) for x in scores]
        total: float = sum(scores)
        scores = [x / total * self.breadth for x in scores]

        int_scores: List[int] = [int(x) for x in scores]
        remainder: int = self.breadth - sum(int_scores)

        float_scores: List[Tuple[float, int]] = [
            (int(x) - x, i) for i, x in enumerate(scores)
        ]
        float_scores = sorted(float_scores)

        for i in range(remainder):
            int_scores[float_scores[i][1]] += 1

        return int_scores

    def run_on_file(self, file: str) -> Tuple[int, int]:
        name = basename(file)
        self.logger.info(f"Running on {file}")

        file_path = Path(file)
        with file_path.open() as f:
            prg = f.read()

        self.runner.starting_prg = prg
        prg = self.runner.preprocess(prg, self.mode)

        text_description = None
        if self.runner.config.include_text_descriptions:
            text_description_file = (
                file_path.parent / "text-descriptions" / f"{file_path.stem}.txt"
            )
            text_description = text_description_file.read_text()

        self.runner.precheck(prg, self.mode)
        self.tree = Tree(0, prg, "", get_node_counter(), name, self.runner, self.logger)

        verification_result = self.runner.verify_program(
            name, self.tree.counter, self.runner.postprocess(prg)
        )
        if verification_result is not None and verification_result[0]:
            return 0, 0

        current_vertices: List[Tree] = [self.tree]
        current_depth = 1
        generated_total = 0

        while current_depth <= self.depth:
            self.logger.info(f"Running on {file} on depth {current_depth}")
            verified = False
            if current_depth == 1:
                current_vertices, verified = self.tree.generate_children(
                    self.breadth, self.mode, text_description
                )
            else:
                scores = self.gen_scores(current_vertices)
                self.logger.info(
                    f"Scores for {[node.counter for node in current_vertices]}: {scores}"
                )
                new_vertices: List[Tree] = []
                for i in range(self.breadth):
                    vertices, verified = current_vertices[i].generate_children(
                        scores[i], self.mode, text_description
                    )
                    new_vertices += vertices
                    if verified:
                        break
                current_vertices = new_vertices
            generated_total += len(current_vertices)
            if verified:
                self.logger.info(
                    f"Verified {name} with depth {current_depth} and total {generated_total}"
                )
                return current_depth, generated_total
            current_depth += 1

        return -1, generated_total
