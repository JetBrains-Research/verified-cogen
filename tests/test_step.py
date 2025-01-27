import pathlib

from verified_cogen.runners.chain_of_thought import Step


def test_step_file():
    step = Step(pathlib.Path("prompts/humaneval-dafny-cot/steps/001"))
    assert "{program}" in step.question
    assert len(step.examples) == 1
