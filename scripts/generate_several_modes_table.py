# %%
import matplotlib.pyplot as plt
import json
from itertools import accumulate
import pathlib

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
modes = [6]
runs = [0, 1, 2, 3, 4]
for mode in modes:
    print(f"Mode {mode}:")
    paths = [base_name.format(mode=mode, run=run) for run in runs]
    file_cnt = len(files)
    data = [read_result(p) for p in paths]
    tries = [get_tries(d) for d in data]

    max_tries = max(max(t) for t in tries)
    cnt = [[0] * (max_tries + 1) for _ in range(len(runs) + 1)]
    for i, t in enumerate(tries):
        for tt in t:
            cnt[i][tt] += 1
            cnt[-1][tt] += 1
    cnt[-1] = [x / len(runs) for x in cnt[-1]]
    cumulative = [list(accumulate(c)) for c in cnt]
    perc = [[100 * (c / file_cnt) for c in cm] for cm in cumulative]

    for run in runs:
        print(f"Run {run}: {cumulative[run][-1]} / {file_cnt}")

    print("Average:")
    print(f"{round(cumulative[-1][-1], 1)} / {file_cnt}")
    print(f"{round(perc[-1][-1])}% of the files were successfully verified")

    best_tries = get_best_tries(data)
    cnt_best = [0] * (max_tries + 1)
    for t in best_tries:
        cnt_best[t] += 1
    cumulative_best = list(accumulate(cnt_best))
    perc_best = [100 * (c / file_cnt) for c in cumulative_best]
    print("Unique:")
    print(f"{cumulative_best[-1]} / {file_cnt}")
    print(f"{round(perc_best[-1], 2)}% of the files were successfully verified")
# fig, ax = plt.subplots()  # type: ignore
# plt.title("Percentage of files verified")  # type: ignore
# plt.xlabel("Number of tries")  # type: ignore
# plt.ylabel("Percentage of files")  # type: ignore
# ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x}%"))  # type: ignore
# ax.plot(perc)  # type: ignore
# # %%
# plt.show()
# %%

