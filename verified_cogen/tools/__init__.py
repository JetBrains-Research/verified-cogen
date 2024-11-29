import logging
import pathlib
import re
import sys
from typing import Optional

import appdirs  # type: ignore


def get_cache_dir() -> str:
    return appdirs.user_cache_dir("verified-cogen", "jetbrains.research")  # type: ignore


def basename(path: str):
    return pathlib.Path(path).name


def rename_file(file: pathlib.Path) -> str:
    return " ".join(file.stem.split("_")).title()


def ext_glob(filter_by_ext: Optional[str]) -> str:
    if filter_by_ext is None:
        return "[!.]*"
    return f"[!.]*.{filter_by_ext}"


def extension_from_file_list(files: list[pathlib.Path]) -> str:
    extension = files[0].suffix[1:]
    if (
        different := next((f for f in files if f.suffix[1:] != extension), None)
    ) is not None:
        raise ValueError(
            f"Found files different extensions: {files[0].name} and {different.name}, please use a single extension"
        )
    return extension


def pprint_stat(name: str, stat: int, total: int, runs: int = 1):
    print(f"{name}: {stat / runs} ({stat / (total * runs) * 100:.2f}%)")


def tabulate_list(lst: list[str]) -> str:
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


def register_output_handler(logger: logging.Logger):
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def compare_errors(error1: str, error2: str):
    pattern = r"\(.*?\.py"
    pattern_time = r"Verification took \d+\.\d+ seconds\."

    cleaned_error1 = re.sub(pattern, "(", error1).strip()
    cleaned_error1 = re.sub(pattern_time, "", cleaned_error1).strip()

    cleaned_error2 = re.sub(pattern, "(", error2).strip()
    cleaned_error2 = re.sub(pattern_time, "", cleaned_error2).strip()

    return cleaned_error1 == cleaned_error2


def rewrite_error(prg: str, error: str) -> str:
    lines = error.splitlines()
    res_error = ""
    for line in lines:
        res_error += line + "\n"
        position = line.find(".py@")
        if position != -1:
            position += 3
            pos_end = line.find(".", position)
            num_st = int(line[position + 1 : pos_end]) - 1
            num_end = num_st + 1
            position = line.find("--", position)

            if position != -1:
                position += 1
                pos_end = line.find(".", position)
                num_end = int(line[position + 1 : pos_end])

            res_error += "Error occurred on the following line(s)\n"
            ln = "\n".join(prg.splitlines()[num_st:num_end])
            res_error += ln + "\n"
    return res_error
