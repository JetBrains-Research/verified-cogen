import argparse
import json
import logging
import os

from pathlib import Path
from typing import Optional
from verified_cogen.tools.verifier import Verifier

from verified_cogen.llm import LLM

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

EXAMPLES_PROMPT = "Before we start, here are some examples of correctly verified programs using Verus:"

EXAMPLES = [
    "has_close_elements",
    "index_wise_addition",
    "smallest_missing_number",
    "is_non_prime",
    "unique_better",
]


def construct_examples() -> str:
    result = EXAMPLES_PROMPT + "\n"
    for example in EXAMPLES:
        with open(f"RustBench/ground_truth/{example}.rs", "r") as f:
            result += f.read() + "\n"
    return result


INVARIANTS_JSON_PROMPT = """Given the following Rust program, output Verus invariants that should go into the `while` loop.
Ensure that the invariants are as comprehensive as they can be.
Even if you think some invariant is not totally necessary, better add it than not.
Respond with a JSON array of strings, representing the invariants.
Remember that invariants should not contain a word `invariant` in them, just the expression.
The program:
{program}
"""

REMOVE_FAILED_INVARIANTS_PROMPT = """Some of the provided invariants either have syntax errors or failed to verify.
Could you please remove the invariants that failed to verify and provide the rest again as a JSON array of strings?

Here's an error from the verifier:
{error}
"""


def reset_llm(llm: LLM):
    llm.had_errors = False
    llm.user_prompts = []
    llm.responses = []
    llm.user_prompts.append(construct_examples())


def collect_invariants(args, prg: str):
    result_invariants = []
    for temperature in range(0, 5):
        llm = LLM(
            grazie_token=args.grazie_token,
            profile=args.profile,
            prompt_dir=args.prompt_dir,
            temperature=temperature / 10,
        )
        reset_llm(llm)

        llm.user_prompts.append(INVARIANTS_JSON_PROMPT.format(program=prg))
        response = llm._make_request()
        try:
            invariants = json.loads(response)
            result_invariants.extend(invariants)
            log.info(
                f"Got {len(invariants)} invariants at temperature {temperature / 10.0}"
            )
        except json.JSONDecodeError:
            print("Error parsing response as JSON")
            print(response)
            continue
    return list(set(result_invariants))


def remove_failed_invariants(
    llm: LLM, invariants: list[str], err: str
) -> Optional[list[str]]:
    llm.user_prompts.append(REMOVE_FAILED_INVARIANTS_PROMPT.format(error=err))
    response = llm._make_request()
    try:
        new_invariants = json.loads(response)
        log.info("REMOVED: {}".format(set(invariants).difference(set(new_invariants))))
        return new_invariants
    except json.JSONDecodeError:
        print("Error parsing response as JSON")
        print(response)
        return None


def houdini(
    llm: LLM, verifier: Verifier, prg: str, invariants: list[str]
) -> Optional[list[str]]:
    while len(invariants) > 0:
        reset_llm(llm)
        prg_with_invariants = llm.add(prg, "\n".join(invariants))
        with open("llm-generated/collected.rs", "w") as f:
            f.write(prg_with_invariants)

        log.info(f"Trying to verify with {json.dumps(invariants, indent=2)}")
        (verified, out, err) = verifier.verify(Path("llm-generated/collected.rs"))
        if verified:
            return invariants
        else:
            log.info("Failed to verify invariants")
            log.info("Error: {}".format(err))

            new_invariants = remove_failed_invariants(llm, invariants, err)
            if new_invariants is None:
                return None
            invariants = new_invariants


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--grazie-token", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--prompt-dir", required=True)
    parser.add_argument("--program", required=True)
    parser.add_argument("--verifier-command", required=True)

    args = parser.parse_args()

    with open(args.program, "r") as f:
        prg = f.read()

    invariants = collect_invariants(args, prg)
    log.info("Collected {} invariants".format(len(invariants)))
    log.info("Invariants: {}".format(json.dumps(invariants, indent=4)))

    verifier = Verifier(os.environ["SHELL"], args.verifier_command)
    llm = LLM(
        grazie_token=args.grazie_token,
        profile=args.profile,
        prompt_dir=args.prompt_dir,
        temperature=0.3,
    )
    reset_llm(llm)
    result = houdini(llm, verifier, prg, invariants)
    if result is not None:
        log.info("Vefication successful")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
