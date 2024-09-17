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
cnt = [c / file_cnt for c in cnt]
plt.plot(cnt)
plt.show()

# %%
f"{cnt[-1] * 100}% of the files were successfully verified"
