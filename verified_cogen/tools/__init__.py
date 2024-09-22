import pathlib
import re
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
