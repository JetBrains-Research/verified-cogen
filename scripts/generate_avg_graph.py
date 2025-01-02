# %%
import matplotlib.pyplot as plt
import json
from itertools import accumulate
import pathlib

# %%
path = "verified_cogen/results/tries_Bench_mode6_avg.json"
bench = pathlib.Path("benches/HumanEval-Nagini/Bench")
file_cnt = len(list(bench.glob("*.py")))
with open(path) as f:
    data = json.load(f)

cnt = list(data.values())
for i in range(1, len(cnt)):
    cnt[i] += cnt[i - 1]

print(file_cnt)
cnt = [100 * (c / file_cnt) for c in cnt]

fig, ax = plt.subplots()  # type: ignore
plt.title("Percentage of files verified")  # type: ignore
plt.xlabel("Number of tries")  # type: ignore
plt.ylabel("Percentage of files")  # type: ignore
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x}%"))  # type: ignore
ax.plot(cnt)  # type: ignore
plt.show()

# %%
f"{cnt[-1]}% of the files were successfully verified"
