import pathlib
import re
import textwrap


def basename(path: str):
    return pathlib.Path(path).name


def rename_file(file: pathlib.Path) -> str:
    return " ".join(file.stem.split("_")).title()


def pprint_stat(name: str, stat: int, total: int):
    print(f"{name}: {stat} ({stat / total * 100:.2f}%)")


def tabulate_list(lst: list):
    return "\n\t - " + "\n\t - ".join(lst)


def extract_code_from_llm_output(reply: str) -> str:
    """For fighing LLMs sometimes outputting code in markdown blocks"""
    i = reply.find("<answer>")
    if i != -1:
        reply = reply[i + 8 :]
        i = reply.find("</answer>")
        reply = reply[:i]
        return reply
    i = re.search(r"```\w*", reply)
    if i is not None:
        reply = reply[i.end() :]
        i = reply.find("```")
        reply = reply[:i]
        return reply.strip()
    return reply
