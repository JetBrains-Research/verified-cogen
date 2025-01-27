import argparse
import os
from typing import List, Optional, no_type_check

from verified_cogen.tools.modes import VALID_MODES


class ProgramArgs:
    input: Optional[str]
    dir: Optional[str]
    runs: int
    insert_conditions_mode: str
    bench_type: str
    temperature: float
    verifier_command: str
    verifier_timeout: int
    prompts_directory: str
    grazie_token: str
    llm_profile: str
    tries: int
    retries: int
    output_style: str
    filter_by_ext: Optional[str]
    log_tries: Optional[str]
    output_logging: bool
    remove_conditions: bool
    remove_implementations: bool
    include_text_descriptions: bool
    manual_rewriters: List[str]
    remove_pure: bool

    @no_type_check
    def __init__(self, args):
        self.input = args.input
        self.dir = args.dir
        self.runs = args.runs
        self.insert_conditions_mode = args.insert_conditions_mode
        self.bench_type = args.bench_type
        self.temperature = args.temperature
        self.verifier_command = args.verifier_command
        self.verifier_timeout = args.verifier_timeout
        self.prompts_directory = args.prompts_directory
        self.grazie_token = args.grazie_token
        self.llm_profile = args.llm_profile
        self.tries = args.tries
        self.retries = args.retries
        self.output_style = args.output_style
        self.filter_by_ext = args.filter_by_ext
        self.log_tries = args.log_tries
        self.output_logging = args.output_logging
        self.remove_conditions = args.remove_conditions
        self.remove_implementations = args.remove_implementations
        self.include_text_descriptions = args.include_text_descriptions
        self.manual_rewriters = args.manual_rewriters
        self.remove_pure = args.remove_pure


def get_default_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", required=False)
    parser.add_argument("-d", "--dir", help="directory to run on", required=False)

    parser.add_argument("-r", "--runs", help="number of runs", default=1, type=int)

    parser.add_argument(
        "--insert-conditions-mode",
        help=f"insert conditions using: {', '.join(VALID_MODES)}",
        default="llm",
    )
    parser.add_argument(
        "--bench-type",
        help="benchmark type, available: {invariants, generic, generate, validating, step-by-step, step-by-step-flush}",
        default="invariants",
    )
    parser.add_argument(
        "--temperature",
        help="model temperature",
        default=0,
        type=float,
    )
    parser.add_argument(
        "--verifier-command",
        help="command to run (cmd [file_path]) to verify a file",
        default=os.getenv("VERIFIER_COMMAND"),
    )
    parser.add_argument(
        "--verifier-timeout",
        help="timeout for verifier command",
        default=60,
        type=int,
    )
    parser.add_argument(
        "--prompts-directory",
        help="directory containing prompts",
        default=os.getenv("llm/prompts"),
    )
    parser.add_argument(
        "--grazie-token", help="Grazie JWT token", default=os.getenv("GRAZIE_JWT_TOKEN")
    )
    parser.add_argument(
        "--llm-profile", help="llm profile", default="gpt-4-1106-preview"
    )
    parser.add_argument("--tries", help="number of tries", default=1, type=int)
    parser.add_argument("--retries", help="number of retries", default=0, type=int)
    parser.add_argument(
        "-s", "--output-style", choices=["stats", "full"], default="full"
    )
    parser.add_argument("--filter-by-ext", help="filter by extension", required=False)
    parser.add_argument(
        "--log-tries", help="Save output of every try to given dir", required=False
    )
    parser.add_argument(
        "--output-logging",
        help="Print logs to standard output",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--remove-conditions",
        help="Remove conditions from the program",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--remove-implementations",
        help="Remove implementations from the program",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--include-text-descriptions",
        help="Add text descriptions to the rewrite prompt (only works with step-by-step)",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--manual-rewriters",
        help="Manual rewriters for additional program modifications",
        default=[],
        nargs="+",
    )
    parser.add_argument(
        "--remove-pure",
        help="Remove pure functions from the program",
        default=False,
        action="store_true",
    )
    return parser


def get_args() -> ProgramArgs:
    return ProgramArgs(get_default_parser().parse_args())
