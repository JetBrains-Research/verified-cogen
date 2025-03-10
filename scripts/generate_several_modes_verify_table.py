# %%
from collections import defaultdict

import matplotlib.pyplot as plt
import json
from itertools import accumulate
import pathlib
import re
import pandas as pd
import numpy as np

# %%


def read_bench(d, ext):
    bench = pathlib.Path(d)
    return [x.name.removesuffix(f'.{ext}') for x in bench.glob(f'*.{ext}')]


def read_result(p):
    with open(p) as f:
        return json.load(f)


def get_tries(d):
    return [value for file, value in d.items() if file.removesuffix('.dfy') in files and value != -1]


def get_best_tries(ds):
    return get_tries({file: min((d[file] for d in ds if d[file] != -1), default=-1) for file in ds[0]})


def get_verifies(d):
    verifies = {}
    for p in pathlib.Path(d).glob('*.json'):
        verifies |= read_result(p)
    return verifies


def collect_verifies(verifies, ext):
    collected = defaultdict(lambda: [0, 0, 0])
    for prg in verifies:
        if 'valid' in prg:
            continue
        prg_base, prg_run = prg.removesuffix(f'.{ext}').rsplit('.', maxsplit=1)
        prg_valid = f"{prg_base}_valid.{prg_run}.{ext}"
        if not verifies[prg]:
            collected[prg_base][0] += 1
        elif not verifies[prg_valid]:
            collected[prg_base][1] += 1
        else:
            collected[prg_base][2] += 1
    return {k: tuple(v) for k, v in collected.items()}


# %%
intersect_bench = False
dafny_bench = pathlib.Path("benches/HumanEval-Dafny")
nagini_bench = pathlib.Path("benches/HumanEval-Nagini/Bench")
dafny_files = read_bench("benches/HumanEval-Dafny", "dfy")
nagini_files = read_bench("benches/HumanEval-Nagini/Bench", "py")
shared_files = [x for x in dafny_files if x in nagini_files]
files = shared_files if intersect_bench else dafny_files

# %%
base_name = "results/tries_HumanEval-Dafny_mode{mode}_{run}.json"
dir_base_name = "results/history_HumanEval-Dafny_mode{mode}_{run}"
modes = [5]
runs = [0, 1, 2, 3, 4]
for mode in modes:
    print(f"Mode {mode}:")
    vrf = [get_verifies(dir_base_name.format(mode=mode, run=run)) for run in runs]
    col = [collect_verifies(v, 'dfy') for v in vrf]
    dfs = [pd.DataFrame(c).T for c in col]
    df = pd.concat(dfs)
    df.rename({0: 'unverified', 1: 'verified', 2: 'validated'}, inplace=True, axis=1)

    total = len(df)
    totally_unverified = ((df['verified'] == 0) & (df['validated'] == 0)).sum()
    verified_unvalidated = ((df['verified'] > 0) & (df['validated'] == 0)).sum()
    validated_after_verify = ((df['verified'] > 0) & (df['validated'] > 0)).sum()
    validated_immediately = ((df['verified'] == 0) & (df['validated'] > 0)).sum()
    result_table = pd.DataFrame({
        'unvalidated': {
            'unverified': totally_unverified,
            'verified': verified_unvalidated,
        },
        'validated': {
            'unverified': validated_immediately,
            'verified': validated_after_verify,
        }
    }).T
