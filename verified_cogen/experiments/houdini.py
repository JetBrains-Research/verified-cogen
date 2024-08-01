import argparse
import json
import logging
import os

from typing import Optional
from verified_cogen.runners import LLM_GENERATED_DIR
from verified_cogen.tools import basename
from verified_cogen.tools.verifier import Verifier
from verified_cogen.llm import prompts

from verified_cogen.llm import LLM

log = logging.getLogger(__name__)


def collect_invariants(name: str, grazie_token: str, prompt_dir: str, prg: str):
    func = name[:-3]  # TODO: should depend on the programming language (now strips .rs)
    result_invariants = []
    for model in ["gpt-4o", "anthropic-claude-3.5-sonnet"]:
        for temperature in [0.0, 0.1, 0.4, 0.5, 0.7, 1.0]:
            llm = LLM(
                grazie_token=grazie_token,
                profile=model,
                prompt_dir=prompt_dir,
                temperature=temperature,
            )

            llm.user_prompts.append(
                prompts.produce_invariants_json_prompt(prompt_dir)
                .replace("{program}", prg)
                .replace("{function}", func)
            )
            response = llm._make_request()
            try:
                invariants = json.loads(response)
                result_invariants.extend(invariants)
                log.info(
                    f"Got {len(invariants)} invariants at temperature {temperature}, model {model}"
                )
            except json.JSONDecodeError:
                print("Error parsing response as JSON")
                print(response)
                continue
    return list(set(result_invariants))


def remove_failed_invariants(
    llm: LLM, invariants: list[str], err: str
) -> Optional[list[str]]:
    llm.user_prompts.append(
        prompts.remove_failed_invariants_prompt(llm.prompt_dir).format(error=err)
    )
    response = llm._make_request()
    try:
        new_invariants = json.loads(response)
        log.info("REMOVED: {}".format(set(invariants).difference(set(new_invariants))))
        return list(set(new_invariants))
    except json.JSONDecodeError:
        print("Error parsing response as JSON")
        print(response)
        return None


def houdini(
    llm: LLM,
    name: str,
    verifier: Verifier,
    prg: str,
    invariants: list[str],
) -> Optional[str]:
    func = name[:-3]
    log.info(f"Starting Houdini for {func} in file {name}")

    llm.set_system_prompt(
        prompts.houdini_sys_prompt(llm.prompt_dir).replace("{program}", prg)
    )

    while len(invariants) > 0:
        llm.reset()

        prg_with_invariants = llm.add(prg, "\n".join(invariants), func)
        with open(LLM_GENERATED_DIR / name, "w") as f:
            f.write(prg_with_invariants)

        log.info(f"Trying to verify with {json.dumps(invariants, indent=2)}")
        ver_result = verifier.verify(LLM_GENERATED_DIR / name)
        if ver_result is None:
            log.info("Verifier timed out")
            return None

        (verified, out, err) = ver_result
        if verified:
            return prg_with_invariants
        else:
            log.info("Failed to verify invariants")
            log.info("Error: {}".format(err))

            new_invariants = remove_failed_invariants(llm, invariants, out + err)
            if new_invariants is not None and not set(new_invariants).issubset(
                set(invariants)
            ):
                log.error(
                    "New invariants are not a subset of the old invariants, changing to an intersection"
                )
                new_invariants = list(set(new_invariants) & set(invariants))

            if new_invariants is None or set(new_invariants) == set(invariants):
                return None

            invariants = new_invariants


def run_on(
    llm: LLM,
    verifier: Verifier,
    prg: str,
    name: str,
    grazie_token: str,
    prompt_dir: str,
) -> Optional[str]:
    log.info("Running on program: {}".format(name))

    invariants = collect_invariants(name, grazie_token, prompt_dir, prg)
    log.info("Collected {} invariants".format(len(invariants)))
    log.info("Invariants: {}".format(json.dumps(invariants, indent=4)))

    return houdini(llm, name, verifier, prg, invariants)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--grazie-token", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--prompt-dir", required=True)
    parser.add_argument("--program", required=True)
    parser.add_argument("--verifier-command", required=True)

    args = parser.parse_args()

    llm = LLM(
        grazie_token=args.grazie_token,
        profile=args.profile,
        prompt_dir=args.prompt_dir,
        temperature=0.0,
    )

    with open(args.program, "r") as f:
        prg = f.read()

    result = run_on(
        llm,
        Verifier(os.environ["SHELL"], args.verifier_command),
        prg,
        basename(args.program),
        args.grazie_token,
        args.prompt_dir,
    )
    if result is not None:
        print(result)
