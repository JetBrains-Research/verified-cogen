# %%
import matplotlib.pyplot as plt
import json
from itertools import accumulate
import pathlib

# %%


def read_bench(d, ext):
    bench = pathlib.Path(d)
    return [x.name.removesuffix(f'.{ext}') for x in bench.glob(f'*.{ext}')]


# %%

intersect_bench = True

path = "results/dafny_4_comments.json"
dafny_bench = pathlib.Path("benches/HumanEval-Dafny")
nagini_bench = pathlib.Path("benches/HumanEval-Nagini/Bench")
dafny_files = read_bench("benches/HumanEval-Dafny", "dfy")
nagini_files = read_bench("benches/HumanEval-Nagini/Bench", "py")
shared_files = [x for x in dafny_files if x in nagini_files]
files = shared_files if intersect_bench else dafny_files
# %%
file_cnt = len(files)
with open(path) as f:
    data = json.load(f)

tries = [value for file, value in data.items() if file.removesuffix('.dfy') in files and value != -1]
max_tries = max(tries)
cnt = [0] * (max_tries + 1)
for t in tries:
    cnt[t] += 1
cnt = list(accumulate(cnt))
perc = [100 * (c / file_cnt) for c in cnt]

fig, ax = plt.subplots()  # type: ignore
plt.title("Percentage of files verified")  # type: ignore
plt.xlabel("Number of tries")  # type: ignore
plt.ylabel("Percentage of files")  # type: ignore
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x}%"))  # type: ignore
ax.plot(perc)  # type: ignore
# %%
plt.show()
# %%
print(f"{cnt[-1]} / {file_cnt}")
print(f"{round(perc[-1],2)}% of the files were successfully verified")
