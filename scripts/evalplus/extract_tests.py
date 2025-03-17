# %%
import json
import sys
import os
import glob
from pathlib import Path
import subprocess
import shutil
sys.set_int_max_str_digits(100000000)
# %%
with open("benches/HumanEval-Dafny/tests/collected_tests.json") as f:
    tests = json.load(f)

# %%
names = [Path(f).name for f in glob.glob("benches/HumanEval-Dafny/*.dfy")]

name_by_id = {int(n[:3]): n for n in names}

# %%
outer_pattern = "method Main()\n  decreases *\n{{\n{tests}}}"

default_test_pattern = '\t{{var v := {entrypoint}({args}); expect v == {result}, "test {i} failed";}}\n'

two_rets_pattern = '\t{{var s, p := {entrypoint}({args}); expect [s, p] == {result}, "test {i} failed";}}\n'

test_pattern = {
    4: '\t{{var v := {entrypoint}({args}); expect abs(v - {result}) < 0.00001, "test {i} failed";}}\n',
    8: two_rets_pattern,
    20: two_rets_pattern,
    107: two_rets_pattern,
    112: '\t{{var s, p := {entrypoint}({args}); expect (s == {result1} && p == {result2}), "test {i} failed";}}\n',
    136: two_rets_pattern,
    155: two_rets_pattern
}

skips = {58, 69, 84, 90, 92, 116, 119, 127, 145, 146, 148, 151, 158}
# 116, 119, 127, 145, 146, 148, 151?, 158 for rewrite

default_formatter = lambda problem_id, entrypoint, args, result, i: (
    test_pattern.get(problem_id, default_test_pattern).format(
            entrypoint=entrypoint,
            args=', '.join(map(preprocess, args)),
            result=preprocess(result),
            i=i
        )
    )

preprocess_optional = lambda r: f"Some({preprocess(r)})" if r is not None else "None"

optional_result = lambda problem_id, entrypoint, args, result, i: (
        test_pattern.get(problem_id, default_test_pattern).format(
            entrypoint=entrypoint,
            args=', '.join(map(preprocess, args)),
            result=preprocess_optional(result),
            i=i
        )
    )

alternative_formatters = {
    12: optional_result,
    45: lambda problem_id, entrypoint, args, result, i: (
        test_pattern.get(problem_id, default_test_pattern).format(
            entrypoint=entrypoint,
            args=', '.join(map(preprocess, [float(a) for a in args])),
            result=preprocess(result),
            i=i
        )
    ),
    81: lambda problem_id, entrypoint, args, result, i: (
        default_test_pattern.format(
            entrypoint=entrypoint,
            args=', '.join(map(lambda xs: preprocess([float(x) for x in xs]), args)),
            result=preprocess(result),
            i=i
        )
    ),
    87: lambda problem_id, entrypoint, args, result, i: (
        default_test_pattern.format(
            entrypoint=entrypoint,
            args=', '.join(map(preprocess, args)),
            result=preprocess([tuple(x) for x in result]),
            i=i
        )
    ),
    90: optional_result,
    111: lambda problem_id, entrypoint, args, result, i: (
        test_pattern.get(problem_id, default_test_pattern).format(
            entrypoint=entrypoint,
            args=', '.join(map(preprocess, args)),
            result=preprocess(result).replace('"', "'"),
            i=i
        )
    ),
    112: lambda problem_id, entrypoint, args, result, i: (
        test_pattern.get(problem_id, default_test_pattern).format(
            entrypoint=entrypoint,
            args=', '.join(map(preprocess, args)),
            result1=preprocess(result[0]),
            result2=preprocess(result[1]),
            i=i
        )
    ),
    119: lambda problem_id, entrypoint, args, result, i: default_formatter(problem_id, entrypoint, args[0], result, i),
    127: lambda problem_id, entrypoint, args, result, i: (
        test_pattern.get(problem_id, default_test_pattern).format(
                entrypoint=entrypoint,
                args=', '.join(map(preprocess, args[0] + args[1])),
                result=preprocess(result),
                i=i
            )
        ),
    128: optional_result,
    130: lambda problem_id, entrypoint, args, result, i: (
        test_pattern.get(problem_id, default_test_pattern).format(
                entrypoint=entrypoint,
                args=', '.join(map(preprocess, args)),
                result=preprocess([int(r) for r in result]),
                i=i
            )
        ),
    133: lambda problem_id, entrypoint, args, result, i: (
        test_pattern.get(problem_id, default_test_pattern).format(
            entrypoint=entrypoint,
            args=', '.join(map(preprocess, [[float(a) for a in args[0]]])),
            result=preprocess(result),
            i=i
        )
    ),
    136: lambda problem_id, entrypoint, args, result, i: (
        test_pattern.get(problem_id, default_test_pattern).format(
            entrypoint=entrypoint,
            args=', '.join(map(preprocess, args)),
            result=f'[{preprocess_optional(result[0])}, {preprocess_optional(result[1])}]',
            i=i
        )
    ),
    151: lambda problem_id, entrypoint, args, result, i: (
        test_pattern.get(problem_id, default_test_pattern).format(
            entrypoint=entrypoint,
            args=', '.join(map(preprocess, [[float(a) for a in args[0]]])),
            result=preprocess(result),
            i=i
        )
    )
}


def preprocess(s):
    if isinstance(s, float):
        s = round(s, 7)
    if isinstance(s, str):
        s = f'"{s}"'
    if isinstance(s, dict):
        sr = "map["
        for k, v in s.items():
            sr += preprocess(k)
            sr += " := "
            sr += preprocess(v)
            sr += ", "
        if s:
            sr = sr[:-2]
        sr += "]"
        s = sr
    else:
        s = str(s)
    s = s.replace("False", "false").replace("True", "true")
    s = s.replace("'", '"').replace('\n', '\\n')
    return s


def make_test(problem_id: int, problem_data):
    if problem_id not in name_by_id:
        return None
    entrypoint = problem_data["entrypoint"]
    test_lines = ""
    for i, (args, res) in enumerate(problem_data["base"]):
        test_lines += (alternative_formatters.get(problem_id, default_formatter)
                       (problem_id, entrypoint, args, res, i))
    return outer_pattern.format(tests=test_lines)


# %%
for pid, pd in tests.items():
    pid = int(pid.rsplit("/", 1)[1])
    if pid in skips:
        continue
    ptest = make_test(pid, pd)
    if ptest is not None:
        with open(f"scripts/evalplus/tests/{name_by_id[pid]}", "w") as f:
            f.write(ptest)
# %%

test_dir = Path("scripts/evalplus/tests/")
for pid, pd in tests.items():
    pid = int(pid.rsplit("/", 1)[1])
    if pid not in name_by_id:
        continue
    if pid in skips:
        continue
    working_dir = test_dir / "working" / Path(name_by_id[pid]).stem
    working_dir.mkdir(parents=True, exist_ok=True)
    test_file = working_dir / f"{name_by_id[pid]}"
    if test_file.exists():
        continue
    with open(f"benches/HumanEval-Dafny/{name_by_id[pid]}") as f:
        prg = f.read()
    ptest = make_test(pid, pd)
    if ptest is not None:
        with open(test_file, "w") as f:
            f.write(prg)
            f.write("\n")
            f.write(ptest)
        try:
            res = subprocess.run(
                f'dafny run --no-verify --allow-warnings "{test_file}"',
                capture_output=True,
                shell=True,
                timeout=60
            )
        except subprocess.TimeoutExpired as e:
            print(name_by_id[pid], "timeout")
            shutil.rmtree(working_dir)
            continue
        if res.returncode != 0:
            print(name_by_id[pid], "fail")
            print(res.stdout.decode("utf-8"))
            # shutil.rmtree(working_dir)
            break
        else:
            print(name_by_id[pid], "success")
