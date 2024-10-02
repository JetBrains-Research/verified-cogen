# %%
import matplotlib.pyplot as plt
import json
from itertools import accumulate
import pathlib

# %%
path = "../results/tries_HumanEval-Dafny.json"
bench = pathlib.Path("../benches/HumanEval-Dafny")
file_cnt = len(list(bench.glob("*.dfy")))
with open(path) as f:
    data = json.load(f)

tries = data.values()
max_tries = max(tries)
cnt = [0] * (max_tries + 1)
for t in tries:
    cnt[t] += 1
cnt = list(accumulate(cnt))
cnt = [100 * (c / file_cnt) for c in cnt]

fig, ax = plt.subplots()  # type: ignore
plt.title("Percentage of files verified")  # type: ignore
plt.xlabel("Number of tries")  # type: ignore
plt.ylabel("Percentage of files")  # type: ignore
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x}%"))  # type: ignore
ax.plot(cnt)  # type: ignore

# %%
f"{cnt[-1] * 100}% of the files were successfully verified"
