from pathlib import Path
from typing import Tuple, List

import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes import DiGraph


def paint_tree(edges: List[Tuple[int, int]], file: Path):
    g: DiGraph[int] = nx.DiGraph()

    g.add_edges_from(edges)

    for layer, nodes in enumerate(nx.topological_generations(g)):
        for node in nodes:
            g.nodes[node]["layer"] = layer

    pos = nx.multipartite_layout(g, subset_key="layer")
    plt.figure()
    nx.draw(g, pos, with_labels=True)
    plt.savefig(file, format="png", dpi=300)
    plt.close()
