"""Building and saving the graphs that the random walk runs on."""

import matplotlib.pyplot as plt
import networkx as nx

GRAPH_FILE = 'output_graph.txt'


class GraphBuilder:
    """Builds a graph with networkx, draws it, and saves its edge list to disk."""

    def __init__(self):
        self.v = 0  # number of nodes
        self.e = 0  # number of edges (or the degree, for regular graphs)

    def regular_graph(self):
        """Build a random d-regular graph (`self.e` is the degree here)."""
        self._save_and_show(nx.random_regular_graph(self.e, self.v))

    def tree_graph(self):
        """Build a uniformly random labeled tree with `self.v` nodes."""
        self._save_and_show(nx.random_labeled_tree(self.v))

    def random_graph(self):
        """Build a G(n, m) random graph with `self.v` nodes and `self.e` edges."""
        self._save_and_show(nx.gnm_random_graph(self.v, self.e))

    def _save_and_show(self, G):
        """Write the graph's adjacency list to GRAPH_FILE, then display the graph.

        An adjacency list (rather than an edge list) is used so that isolated
        nodes survive the round trip to disk.
        """
        nx.write_adjlist(G, GRAPH_FILE)
        fig, ax = plt.subplots()
        nx.draw(G, ax=ax, with_labels=True)
        ax.set_title('Generated graph (close this window to continue)')
        plt.show()
        plt.close(fig)
