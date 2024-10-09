from verified_cogen.tools.dafny_separate import dafny_separate
from verified_cogen.tools.verifier import Verifier
from os import environ
from pathlib import Path


EXPECTED_VALIDATOR_ERRORS = """\
tests/sources/dafny_wrong_postconditions.dfy(163,51): Error: a postcondition could not be proved on this return path
    |
163 | { var ret0 := separate_paren_groups(paren_string); return ret0; }
    |                                                    ^^^^^^

tests/sources/dafny_wrong_postconditions.dfy(161,10): Related location: this is the postcondition that could not be proved
    |
161 |   ensures forall k :: 0 <= k < |res| ==> InnerDepthsPositive(res[k])
    |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/sources/dafny_wrong_postconditions.dfy(163,51): Error: a postcondition could not be proved on this return path
    |
163 | { var ret0 := separate_paren_groups(paren_string); return ret0; }
    |                                                    ^^^^^^

tests/sources/dafny_wrong_postconditions.dfy(160,10): Related location: this is the postcondition that could not be proved
    |
160 |   ensures forall k :: 0 <= k < |res| ==> ParenthesesDepth(res[k], 0, |res[k]|) == 0
    |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""


def test_separate():
    verifier = Verifier(
        shell=environ["SHELL"], verifier_cmd="dafny verify --allow-warnings", timeout=10
    )

    errors = verifier.verify(Path("tests/sources/dafny_wrong_postconditions.dfy"))
    assert errors is not None
    assert not errors[0]

    non_validator_errors, validator_errors = dafny_separate(errors[1] + errors[2])
    assert non_validator_errors == ""
    assert validator_errors.strip() == EXPECTED_VALIDATOR_ERRORS.strip()
