from pathlib import Path
from typing import Tuple, List

import networkx as nx
import matplotlib.pyplot as plt


def paint_tree(edges: List[Tuple[int, int]], file: Path):
    G = nx.DiGraph()

    G.add_edges_from(edges)

    for layer, nodes in enumerate(nx.topological_generations(G)):
        for node in nodes:
            G.nodes[node]["layer"] = layer

    pos = nx.multipartite_layout(G, subset_key="layer")
    plt.figure()
    nx.draw(G, pos, with_labels=True)
    plt.savefig(file, format="png", dpi=300)
    plt.close()
