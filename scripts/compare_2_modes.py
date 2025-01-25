# %%
import matplotlib.pyplot as plt
import json
from itertools import accumulate
import pathlib
import seaborn as sns
import pandas as pd

# %%


def read_result(file):
    with open(file) as f:
        return {name[:3]: t if t >= 0 else 99 for name, t in json.load(f).items()}


# %%


def plot_results_heatmap(results_dict, width=35):
    df = pd.DataFrame.from_dict({
        source: entry_dict
        for source, entry_dict in results_dict.items()
    }, orient='index')

    # Create the heatmap
    plt.figure(figsize=(width, 4))
    sns.heatmap(
        df,
        cmap='YlOrRd',  # Color scheme - you can change this
        annot=True,  # Show numbers in cells
        fmt='d',  # Format as integers
        cbar_kws={'label': 'Result'}
    )

    plt.title('Results Heatmap')
    plt.xlabel('Entries')
    plt.ylabel('Sources')
    plt.tight_layout()


# %%
data = pathlib.Path('verified_cogen/results/overall/mode1')
results = {str(x.name).removesuffix(".json"): read_result(x) for x in sorted(data.glob('*.json'))}

print(results)

# %%
all_tasks = list(next(iter(results.values())).keys())
solve_count = {t: sum(r[t] <= 10 for r in results.values()) for t in all_tasks}

print(solve_count)
# %%
data1 = pathlib.Path('verified_cogen/results/without_fixing/all')
results1 = {str(x.name).removesuffix(".json"): read_result(x) for x in sorted(data1.glob('*.json'))}

print(results1)

# %%
solve_count1 = {t: sum(r[t] <= 10 for r in results1.values()) for t in all_tasks}

print(solve_count1)

# %%
print(len([t for t in all_tasks if solve_count[t] > 0]))
print(len([t for t in all_tasks if solve_count1[t] > 0]))

# %%

common = {t for t in all_tasks if solve_count[t] > 0 and solve_count1[t] > 0}

only1 = {t for t in all_tasks if solve_count[t] > 0 and solve_count1[t] == 0}
only2 = {t for t in all_tasks if solve_count[t] == 0 and solve_count1[t] > 0}

print(common)
print(only1)
print(only2)