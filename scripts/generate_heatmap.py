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
data = pathlib.Path('heatmap_data')
results = {str(x.name).removesuffix(".json"): read_result(x) for x in sorted(data.glob('*.json'))}
# %%
plot_results_heatmap(results, width=33)
plt.show()

# %%
all_tasks = list(next(iter(results.values())).keys())
solve_count = {t: sum(r[t] <= 10 for r in results.values()) for t in all_tasks}
# %%
nontrivial_tasks = [t for t in all_tasks if 0 < solve_count[t] < len(results)]
nontrivial_results = {s: {t: r[t] for t in nontrivial_tasks} for s, r in results.items()}
variant_tasks = [t for t in all_tasks if 2 <= solve_count[t] <= len(results) - 2]
variant_results = {s: {t: r[t] for t in variant_tasks} for s, r in results.items()}
# %%
plot_results_heatmap(nontrivial_results, width=19)
plt.show()
# %%
plot_results_heatmap(variant_results, width=10)
plt.show()