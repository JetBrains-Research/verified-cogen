import argparse
import json
import logging
from typing import Optional, no_type_check

from verified_cogen.llm import LLM
from verified_cogen.runners import LLM_GENERATED_DIR
from verified_cogen.tools import basename
from verified_cogen.tools.verifier import Verifier

log = logging.getLogger(__name__)


class ProgramArgs:
    grazie_token: str
    profile: str
    prompt_dir: str
    program: str
    verifier_command: str

    @no_type_check
    def __init__(self, *args):
        (
            self.grazie_token,
            self.profile,
            self.prompt_dir,
            self.program,
            self.verifier_command,
        ) = args


INVARIANTS_JSON_PROMPT = """Given the following Rust program, output Verus invariants that should go into the `while` loop
in the function {function}.
Ensure that the invariants are as comprehensive as they can be.
Even if you think some invariant is not totally necessary, better add it than not.
Don't be afraid of using disjunctions if you see that some invariant is not true, for example, at the beginning of the loop.
Respond with a JSON array of strings, representing the invariants.
Remember that invariants should not contain a word `invariant` in them, just the expression.
Here are some examples of verified functions:
```rust
fn incr_list(l: Vec<i32>) -> (result: Vec<i32>)
    requires
        forall|i: int| 0 <= i < l.len() ==> l[i] + 1 <= i32::MAX,  // avoid overflow

    ensures
        result.len() == l.len(),
        forall|i: int| 0 <= i < l.len() ==> #[trigger] result[i] == l[i] + 1,
{
    let mut result = Vec::new();
    for i in 0..l.len()
        invariant
            forall|i: int| 0 <= i < l.len() ==> l[i] + 1 <= i32::MAX,
            result.len() == i,
            forall|j: int| 0 <= j < i ==> #[trigger] result[j] == l[j] + 1,
    {
        result.push(l[i] + 1);
    }
    result
}
```

```rust
#[verifier::loop_isolation(false)]
fn unique(a: &[i32]) -> (result: Vec<i32>)
    requires
        forall|i: int, j: int|
            #![trigger a[i], a[j]]
            0 <= i && i < j && j < a.len() ==> a[i] <= a[j],
    ensures
        forall|i: int, j: int|
            #![trigger result[i], result[j]]
            0 <= i && i < j && j < result.len() ==> result[i] < result[j],
{
    let mut result: Vec<i32> = Vec::new();
    let mut i = 0;
    while i < a.len()
        invariant
            0 <= i <= a.len(),
            forall|k: int, l: int|
                #![trigger result[k], result[l]]
                0 <= k && k < l && l < result.len() ==> result[k] < result[l],
            forall|k: int|
                #![trigger result[k]]
                0 <= k && k < result.len() ==> exists|m: int| 0 <= m < i && result[k] == a[m],
    {
        if result.len() == 0 || result[result.len() - 1] != a[i] {
            assert(result.len() == 0 || result[result.len() - 1] < a[i as int]);
            result.push(a[i]);
        }
        i = i + 1;
    }
    result
}
```
The program:
{program}
"""

HOUDINI_SYS_PROMPT = """
You are an expert in a Rust verification framework Verus.
Do not provide ANY explanations. Don't include markdown backticks. Respond only in Rust code when not asked otherwise.
Do not touch any functions other that {function}
You will be working with the following program:
{program}
"""

REMOVE_FAILED_INVARIANTS_PROMPT = """Some of the provided invariants either have syntax errors or failed to verify.
Could you please remove the invariants that failed to verify and provide the rest again as a JSON array of strings?
DO NOT MODIFY THE INVARIANTS OR ADD NEW ONES.

Here's an error from the verifier:
{error}
"""


def collect_invariants(args: ProgramArgs, prg: str) -> list[str]:
    func = basename(args.program)[:-3]
    result_invariants: list[str] = []
    for temperature in [0.0, 0.1, 0.3, 0.4, 0.5, 0.7, 1.0]:
        llm = LLM(
            grazie_token=args.grazie_token,
            profile=args.profile,
            prompt_dir=args.prompt_dir,
            temperature=temperature,
        )

        llm.add_user_prompt(INVARIANTS_JSON_PROMPT.replace("{program}", prg).replace("{function}", func))
        response = llm.make_request()
        try:
            invariants = json.loads(response)
            result_invariants.extend(invariants)
            log.debug(f"Got {len(invariants)} invariants at temperature {temperature}")
        except json.JSONDecodeError:
            print("Error parsing response as JSON")
            print(response)
            continue
    return list(set(result_invariants))


def remove_failed_invariants(llm: LLM, invariants: list[str], err: str) -> Optional[list[str]]:
    llm.add_user_prompt(REMOVE_FAILED_INVARIANTS_PROMPT.format(error=err))
    response = llm.make_request()
    try:
        new_invariants = json.loads(response)
        log.debug("REMOVED: {}".format(set(invariants).difference(set(new_invariants))))
        return new_invariants
    except json.JSONDecodeError:
        print("Error parsing response as JSON")
        print(response)
        return None


def houdini(args: ProgramArgs, verifier: Verifier, prg: str, invariants: list[str]) -> Optional[list[str]]:
    func = basename(args.program).strip(".rs")
    log.info(f"Starting Houdini for {func} in file {args.program}")
    while len(invariants) > 0:
        llm = LLM(
            grazie_token=args.grazie_token,
            profile=args.profile,
            prompt_dir=args.prompt_dir,
            temperature=0.0,
            system_prompt=HOUDINI_SYS_PROMPT.replace("{program}", prg).replace("{function}", func),
        )

        prg_with_invariants = llm.add(prg, "\n".join(invariants), func)
        with open(LLM_GENERATED_DIR / "collected.rs", "w") as f:
            f.write(prg_with_invariants)

        log.debug(f"Trying to verify with {json.dumps(invariants, indent=2)}")
        ver_result = verifier.verify(LLM_GENERATED_DIR / "collected.rs")
        if ver_result is None:
            log.info("Verifier timed out")
            return None

        (verified, out, err) = ver_result
        if verified:
            return invariants
        else:
            log.info("Failed to verify invariants")
            log.debug("Error: {}".format(err))

            new_invariants = remove_failed_invariants(llm, invariants, out + err)
            if new_invariants is None or new_invariants == invariants:
                return None
            inv_set = set(invariants)
            is_subset = True
            for inv in set(new_invariants):
                if inv not in inv_set:
                    is_subset = False
                    log.error(f"New invariant {inv} is not a subset of the old invariants")
            if not is_subset:
                log.error("New invariants are not a subset of the old invariants")
                log.error("Old invariants: {}".format(json.dumps(invariants, indent=2)))
                log.error("New invariants: {}".format(json.dumps(new_invariants, indent=2)))
                raise ValueError("New invariants are not a subset of the old invariants")
            invariants = new_invariants


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--grazie-token", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--prompt-dir", required=True)
    parser.add_argument("--program", required=True)
    parser.add_argument("--verifier-command", required=True)

    args = ProgramArgs(*parser.parse_args())

    log.info("Running on program: {}".format(args.program))

    with open(args.program, "r") as f:
        prg = f.read()

    invariants = collect_invariants(args, prg)
    log.info("Collected {} invariants".format(len(invariants)))
    log.debug("Invariants: {}".format(json.dumps(invariants, indent=4)))

    verifier = Verifier(args.verifier_command)
    result = houdini(args, verifier, prg, invariants)
    if result is not None:
        log.info("Vefication successful")
        log.debug(json.dumps(result, indent=2))
    else:
        log.error("Verification failed")


if __name__ == "__main__":
    main()
