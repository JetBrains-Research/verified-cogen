import argparse
import multiprocessing
import os
from typing import List, Optional, no_type_check

from verified_cogen.tools.modes import VALID_MODES


class ProgramArgsMultiple:
    input: Optional[str]
    dir: Optional[str]
    runs: int
    insert_conditions_mode: str
    bench_types: list[str]
    temperature: float
    verifier_command: str
    verifier_timeout: int
    prompts_directory: List[str]
    modes: List[str]
    skip_failed: bool
    grazie_token: str
    llm_profile: str
    tries: int
    retries: int
    output_style: str
    filter_by_ext: Optional[str]
    log_tries: Optional[str]
    output_logging: bool
    manual_rewriters: List[str]
    max_jobs: int
    shell_validator: List[str]

    @no_type_check
    def __init__(self, args):
        self.input = args.input
        self.dir = args.dir
        self.runs = args.runs
        self.insert_conditions_mode = args.insert_conditions_mode
        self.bench_types = args.bench_types
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
        self.manual_rewriters = args.manual_rewriters
        self.modes = args.modes
        self.skip_failed = args.skip_failed
        self.max_jobs = args.max_jobs
        self.shell_validator = args.shell_validator


def get_default_parser_multiple():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", required=False)
    parser.add_argument("-d", "--dir", help="directory to run on", required=False)

    parser.add_argument("-r", "--runs", help="number of runs", default=1, type=int)
    parser.add_argument(
        "-j",
        "--max-jobs",
        help="maximum number of parallel jobs",
        default=multiprocessing.cpu_count(),
        type=int,
    )

    parser.add_argument(
        "--insert-conditions-mode",
        help=f"insert conditions using: {', '.join(VALID_MODES)}",
        default="llm",
    )
    parser.add_argument(
        "--bench-types",
        help="benchmark type, available: {invariants, generic, generate, validating, step-by-step, step-by-step-flush}",
        default=[],
        nargs="+",
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
        help="directories containing prompts",
        default=[],
        nargs="+",
    )
    parser.add_argument(
        "--skip-failed",
        help="Skip failed files",
        default=False,
        action="store_true",
    )
    parser.add_argument("--grazie-token", help="Grazie JWT token", default=os.getenv("GRAZIE_JWT_TOKEN"))
    parser.add_argument("--llm-profile", help="llm profile", default="gpt-4-1106-preview")
    parser.add_argument("--tries", help="number of tries", default=1, type=int)
    parser.add_argument("--retries", help="number of retries", default=0, type=int)
    parser.add_argument("-s", "--output-style", choices=["stats", "full"], default="full")
    parser.add_argument("--filter-by-ext", help="filter by extension", required=False)
    parser.add_argument("--log-tries", help="Save output of every try to given dir", required=False)
    parser.add_argument(
        "--output-logging",
        help="Print logs to standard output",
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
        "--shell-validator",
        help="Shell arguments to run validator",
        default=[],
        nargs="+",
    )
    parser.add_argument(
        "--modes",
        help="modes",
        default=[],
        nargs="+",
    )
    return parser


def get_args() -> ProgramArgsMultiple:
    return ProgramArgsMultiple(get_default_parser_multiple().parse_args())
