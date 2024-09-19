import argparse
import os

from verified_cogen.tools.modes import VALID_MODES


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
        help="benchmark type, available: {invariants, generic, generate, validating}",
        default="invariants",
    )
    parser.add_argument("--temperature", help="model temperature", default=0, type=int)
    parser.add_argument("--shell", help="shell", default=os.getenv("SHELL"))
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
    parser.add_argument("--filter-by-ext", help="filter by extension", default=None)
    parser.add_argument(
        "--log-tries", help="Save output of every try to given dir", default=None
    )
    parser.add_argument(
        "--output-logging", help="Print logs to standard output", default=False
    )
    return parser


def get_args():
    return get_default_parser().parse_args()
