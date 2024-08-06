import argparse
from verified_cogen.tools.modes import VALID_MODES
import os


def get_args():
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
        help="benchmark type, available: {invariants, generic, generate}",
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
    return parser.parse_args()
