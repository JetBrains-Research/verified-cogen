from typing import Any, Optional


class Singleton:
    _instance = None

    def __new__(cls, *args: list[Any], **kwargs: dict[str, Any]):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


class PromptCache(Singleton):
    cache: dict[str, str] = {}

    def __init__(self, *args: list[Any], **kwargs: dict[str, Any]):
        self.cache = {}

    def get(self, key: str) -> Optional[str]:
        return self.cache.get(key, None)

    def set(self, key: str, value: str):
        self.cache[key] = value


prompt_cache = PromptCache()


def read_prompt(name: str) -> str:
    if (cached := prompt_cache.get(name)) is not None:
        return cached

    with open(name) as f:
        prompt = f.read()
        prompt_cache.set(name, prompt)
        return prompt


def sys_prompt(prompt_dir: str) -> str:
    return read_prompt(f"{prompt_dir}/sys.txt")


def produce_prompt(prompt_dir: str) -> str:
    return read_prompt(f"{prompt_dir}/produce.txt")


def add_prompt(prompt_dir: str) -> str:
    return read_prompt(f"{prompt_dir}/add.txt")


def rewrite_prompt(prompt_dir: str) -> str:
    return read_prompt(f"{prompt_dir}/rewrite.txt")


def ask_for_fixed_prompt(prompt_dir: str) -> str:
    return read_prompt(f"{prompt_dir}/ask_for_fixed.txt")


def ask_for_fixed_had_errors_prompt(prompt_dir: str) -> str:
    return read_prompt(f"{prompt_dir}/ask_for_fixed_had_errors.txt")


def ask_for_timeout_prompt(prompt_dir: str) -> str:
    return read_prompt(f"{prompt_dir}/timeout.txt")


def invalid_helpers_prompt(prompt_dir: str) -> str:
    return read_prompt(f"{prompt_dir}/invalid_helpers.txt")


def helpers_prompt(prompt_dir: str) -> str:
    return read_prompt(f"{prompt_dir}/helpers.txt")
