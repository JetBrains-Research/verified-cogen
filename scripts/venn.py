# %%
import json
import pathlib
from matplotlib import pyplot as plt
from matplotlib_venn import venn3, venn3_circles
from matplotlib_venn.layout.venn3 import DefaultLayoutAlgorithm
from venny4py.venny4py import venny4py
# %%
languages = ['dafny', 'nagini', 'verus']
mode = 6
# %%


def get_sources(lang):
    p = pathlib.Path(f"./overall_{lang}")
    return [f for f in p.glob(f"./**/*_mode{mode}_*.json") if 'avg' not in str(f)]


sources = {lang: get_sources(lang) for lang in languages}
# %%


def parse_source(src):
    with open(src) as f:
        data = json.load(f)
    return {int(k[:3]): v if v <= 5 else -1 for k, v in data.items()}


results = {lang: [parse_source(src) for src in srcs] for lang, srcs in sources.items()}
# %%


def agg_sources(srcs):
    return {k: min((src[k] for src in srcs if src[k] != -1), default=-1) for k in srcs[0].keys()}


unique = {lang: agg_sources(srcs) for lang, srcs in results.items()}
# %%


def intersect_langs(lngs):
    ks = unique[lngs[0]].keys()
    for lng in lngs:
        ks &= unique[lng].keys()
    return {k: all(unique[lng][k] >= 0 for lng in lngs) for k in ks}


dafny = intersect_langs(["dafny"])
nagini = intersect_langs(["nagini"])
verus = intersect_langs(["verus"])
dafny_nagini = intersect_langs(["dafny", "nagini"])
dafny_verus = intersect_langs(["dafny", "verus"])
nagini_verus = intersect_langs(["nagini", "verus"])
dafny_nagini_verus = intersect_langs(["dafny", "nagini", "verus"])

# %%
# v = venn3(
#     (set(dafny.keys()), set(nagini.keys()), set(verus.keys())),
#     set_labels=("Dafny", "Naigni", "Verus"),
#     layout_algorithm=DefaultLayoutAlgorithm(fixed_subset_sizes=(1,1,1,1,1,1,1))
# )
# v.get_patch_by_id('111').set_color('grey')
# v.get_label_by_id('100').set_label('Dafny')
# v.get_label_by_id('010').set_label('Nagini')
# v.get_label_by_id('001').set_label('Verus')
# plt.show()
# %%
# venny4py(
#     sets={
#         'Dafny': set(dafny.keys()),
#         'Nagini': set(nagini.keys()),
#         'Verus': set(verus.keys())
#     }
# )
# plt.title("Benchmark size")
# plt.show()
# %%
venny4py(
    sets={
        'Dafny': {k for k, v in dafny.items() if v},
        'Nagini': {k for k, v in nagini.items() if v},
        'Verus': {k for k, v in verus.items() if v}
    }
)
plt.title(f"Programs verified (mode {mode}, 5 tries)")
# plt.show()
plt.savefig(f"venn_mode{mode}.svg")