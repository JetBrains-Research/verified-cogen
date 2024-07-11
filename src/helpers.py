import re
import textwrap
from modes import Mode
import pathlib
from llm import LLM


def basename(path: str):
    return pathlib.Path(path).name


def rename_file(file: pathlib.Path) -> str:
    return " ".join(file.stem.split("_")).title()


def pprint_stat(name: str, stat: int, total: int):
    print(f"{name}: {stat} ({stat / total * 100:.2f}%)")


def tabulate_list(lst: list):
    return "\n\t - " + "\n\t - ".join(lst)
