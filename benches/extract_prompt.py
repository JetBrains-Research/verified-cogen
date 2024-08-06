#! /usr/bin/env python3

from sys import stdin
from textwrap import dedent

full_test = stdin.read()

prompt_start = full_test.find('"""')
if prompt_start == -1:
    prompt_start = full_test.find("'''")
    if prompt_start == -1:
        raise ValueError("No prompt found")
    prompt_end = full_test.find("'''", prompt_start + 3)
else:
    prompt_end = full_test.find('"""', prompt_start + 3)


print(dedent(full_test[prompt_start + 3 : prompt_end].replace('\n    ', '\n')))
