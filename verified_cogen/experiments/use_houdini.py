import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import click

from verified_cogen.llm import LLM
from verified_cogen.llm.prompts import produce_prompt, read_prompt, sys_prompt
from verified_cogen.runners import LLM_GENERATED_DIR
from verified_cogen.runners.languages import LanguageDatabase, register_basic_languages
from verified_cogen.runners.languages.language import AnnotationType
from verified_cogen.tools import (
    basename,
    extension_from_file_list,
    extract_code_from_llm_output,
)
from verified_cogen.tools.verifier import Verifier

log = logging.getLogger(__name__)


@dataclass
class ProgramArgs:
    grazie_token: str
    profile: str
    prompt_dir: str
    program: str
    verifier_command: str


def collect_invariants(args: ProgramArgs, prg: str) -> list[str]:
    func = basename(args.program)[:-3]
    result_invariants: list[str] = []
    invariants_prompt = produce_prompt(args.prompt_dir)

    for temperature in [0.0, 0.1, 0.3, 0.4, 0.5, 0.7, 1.0]:
        llm = LLM(
            grazie_token=args.grazie_token,
            profile=args.profile,
            prompt_dir=args.prompt_dir,
            temperature=temperature,
            system_prompt=sys_prompt(args.prompt_dir),
        )

        llm.add_user_prompt(invariants_prompt.replace("{program}", prg).replace("{function}", func))
        response = extract_code_from_llm_output(llm.make_request())
        try:
            invariants = json.loads(response)
            result_invariants.extend(invariants)
            log.debug(f"Got {len(invariants)} invariants at temperature {temperature}")
        except json.JSONDecodeError:
            print("Error parsing response as JSON")
            print(response)
            continue
    return list(set(result_invariants))


def remove_failed_invariants(llm: LLM, invariants: list[str], err: str, prompt_dir: str) -> Optional[list[str]]:
    remove_prompt = read_prompt(f"{prompt_dir}/remove_failed_invariants.txt")
    llm.add_user_prompt(remove_prompt.format(error=err))
    response = extract_code_from_llm_output(llm.make_request())
    try:
        new_invariants = json.loads(response)
        log.debug(f"REMOVED: {set(invariants).difference(set(new_invariants))}")
        return new_invariants
    except json.JSONDecodeError:
        print("Error parsing response as JSON")
        print(response)
        return None


def houdini(args: ProgramArgs, verifier: Verifier, prg: str, invariants: list[str]) -> Optional[list[str]]:
    func = basename(args.program).strip(".rs")
    log.info(f"Starting Houdini for {func} in file {args.program}")
    houdini_sys_prompt = sys_prompt(args.prompt_dir)
    while len(invariants) > 0:
        llm = LLM(
            grazie_token=args.grazie_token,
            profile=args.profile,
            prompt_dir=args.prompt_dir,
            temperature=0.0,
            system_prompt=houdini_sys_prompt.replace("{program}", prg).replace("{function}", func),
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
            log.debug(f"Error: {err}")

            new_invariants = remove_failed_invariants(llm, invariants, out + err, args.prompt_dir)
            if new_invariants is None or new_invariants == invariants:
                return None
            inv_set = set(invariants)
            is_subset = True
            for inv in set(new_invariants):
                if inv not in inv_set:
                    is_subset = False
                    log.error(f"New invariant {inv} is not a subset of the old invariants")
            if not is_subset:
                log.warning("New invariants are not a subset of the old invariants")
                log.warning(f"Old invariants: {json.dumps(invariants, indent=2)}")
                log.warning(f"New invariants: {json.dumps(new_invariants, indent=2)}")
                log.warning("Setting new invariants to be an intersection")
                new_invariants = list(set(new_invariants) & set(invariants))
            invariants = new_invariants
            llm.dump_history(Path("history.txt"))


@click.command()
@click.option("--grazie-token", help="Grazie token for authentication")
@click.option("--profile", default="anthropic-claude-3.5-sonnet", help="Profile to use")
@click.option("--prompt-dir", help="Directory containing prompts")
@click.option("--program", help="Program file to verify")
@click.option("--verifier-command", help="Command to run verifier")
def main(
    grazie_token: str,
    profile: str,
    prompt_dir: str,
    program: str,
    verifier_command: str,
):
    register_basic_languages(with_removed=[AnnotationType.INVARIANTS])
    args = ProgramArgs(grazie_token, profile, prompt_dir, program, verifier_command)

    log.info(f"Running on program: {args.program}")

    with open(args.program) as f:
        prg = f.read()

    extension = extension_from_file_list([Path(args.program)])
    language = LanguageDatabase().get(extension)

    prg = language.remove_conditions(prg)
    invariants = collect_invariants(args, prg)
    log.info(f"Collected {len(invariants)} invariants")
    log.info(f"Invariants: {json.dumps(invariants, indent=4)}")

    verifier = Verifier(args.verifier_command)
    result = houdini(args, verifier, prg, invariants)
    if result is not None:
        log.info(f"Vefication successful, see result at {LLM_GENERATED_DIR / 'collected.rs'}")
        log.debug(json.dumps(result, indent=2))
    else:
        log.error("Verification failed")


if __name__ == "__main__":
    main()
