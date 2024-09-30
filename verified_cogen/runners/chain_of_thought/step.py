import pathlib


class Substep:
    question: str
    answer: str

    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer

    def __repr__(self) -> str:
        return f"Substep(question={self.question}, answer={self.answer})"

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Substep):
            return False
        return self.question == value.question and self.answer == value.answer


class Step:
    substeps: list[Substep]
    question: str

    def __init__(self, dir: pathlib.Path):
        self.substeps = []
        for substep in sorted((dir / "examples").iterdir()):
            assert substep.is_dir()
            self.substeps.append(
                Substep(
                    (substep / "question.txt").read_text(),
                    (substep / "answer.txt").read_text(),
                )
            )

        self.question = (dir / "question.txt").read_text()

    def __repr__(self) -> str:
        return f"Step(question={self.question}, substeps={self.substeps})"

    def __str__(self) -> str:
        result = ""
        for substep in self.substeps:
            result += f"===== QUESTION_EXAMPLE =====\n{substep.question}\n===== ANSWER =====\n{substep.answer}\n"
        return result + f"===== QUESTION =====\n{self.question}\n"
