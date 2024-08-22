import re

from verified_cogen.tools.modes import Mode

from verified_cogen.llm import LLM
from verified_cogen.runners import Runner
from verified_cogen.runners.invariants import InvariantRunner

# Regular expression to match Dafny method definitions
method_pattern = re.compile(r'method\s+(\w+)\s*\((.*?)\)\s*returns\s*\((.*?)\)(.*?)\{', re.DOTALL)

def generate_validators(dafny_code):
    """
    Create validator-methods for every method in dafny program

    Example:
    Input:
    method xor(a : char, b : char) returns (result : char)
        ensures result == (if a == b then '0' else '1')
    { if (a == b) { result := '0'; } else { result := '1'; } }
    Output:
    method xor_valid(a : char, b : char) returns (result : char)
        ensures result == (if a == b then '0' else '1')
    { var ret := xor(a, b); return ret; }
    """
    methods = method_pattern.finditer(dafny_code)

    validators = []

    for match in methods:
        method_name = match.group(1)
        parameters = match.group(2)
        returns = match.group(3)
        specs = match.group(4)

        validator = f"method {method_name}_valid({parameters}) returns ({returns}){specs}"
        validator += "{ var ret := "

        validator += f"{method_name}({', '.join(param.split(':')[0].strip() for param in parameters.split(',') if param.strip())});"

        validator += " return ret; }\n"

        validators.append(validator)

    return '\n'.join(validators)


class ValidatingRunner(Runner):

    @classmethod
    def _add_validators(cls, prg: str, inv_prg: str):
        validators = generate_validators(prg)
        val_prg = inv_prg + "\n// ==== verifiers ==== //\n" + validators
        return val_prg

    @classmethod
    def rewrite(cls, llm: LLM, prg: str) -> str:
        return ValidatingRunner._add_validators(prg, InvariantRunner.rewrite(llm, prg))

    @classmethod
    def produce(cls, llm: LLM, prg: str) -> str:
        return ValidatingRunner._add_validators(prg, InvariantRunner.produce(llm, prg))

    @classmethod
    def insert(cls, llm: LLM, prg: str, checks: str, mode: Mode) -> str:
        return ValidatingRunner._add_validators(prg, InvariantRunner.insert(llm, prg, mode))

    @classmethod
    def precheck(cls, prg: str, mode: Mode):
        return InvariantRunner.precheck(prg, mode)