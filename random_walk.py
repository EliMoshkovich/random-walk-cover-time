"""A simple random walk on the saved graph, run until it covers every node."""

import csv
import math
import random

import networkx as nx

from graph_builder import GRAPH_FILE
from walk_view import WalkView

CSV_FILE = 'edge_steps.csv'


class RandomWalk:
    """Loads the last saved graph and walks it until every node has been visited."""

    def __init__(self, path=GRAPH_FILE):
        self.G = nx.read_adjlist(path, nodetype=int)
        self.view = WalkView(self.G)
        self.edges = sorted(self.G.edges())
        self.edge_steps = [0] * len(self.edges)
        # Map both directions of every edge to its index in `self.edges`.
        self.edge_index = {}
        for i, (u, v) in enumerate(self.edges):
            self.edge_index[(u, v)] = i
            self.edge_index[(v, u)] = i

    def run(self, show_graph=False):
        """Run the walk from the lowest-numbered node and return the cover time.

        The cover time is the number of steps (edge traversals) the walk takes
        until every node of the graph has been visited at least once.
        Raises ValueError if the saved graph is empty or not connected.
        """
        nodes = sorted(self.G.nodes())
        if not nodes:
            raise ValueError('The saved graph is empty, so there is nothing to walk on.')
        if not nx.is_connected(self.G):
            raise ValueError('The saved graph is not connected, so a random walk cannot cover it.')
        start = nodes[0]
        self.view.mark_visited(start)
        return self._walk(start, show_graph)

    def _walk(self, start, show_graph):
        """Step from random neighbor to random neighbor until every node is visited.

        Appends the cumulative per-edge traversal counts to CSV_FILE after every
        step and returns the total number of steps taken.
        """
        draw_every = max(math.isqrt(self.G.number_of_nodes()), 1)
        visited = {start}
        current = start
        steps = 0
        with open(CSV_FILE, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(f'{u}-{v}' for u, v in self.edges)
            while len(visited) < self.G.number_of_nodes():
                next_node = random.choice(list(self.G.adj[current]))
                visited.add(next_node)
                self.view.mark_visited(next_node)
                self.edge_steps[self.edge_index[(current, next_node)]] += 1
                steps += 1
                writer.writerow(self.edge_steps)
                if show_graph and steps % draw_every == 0:
                    try:
                        self.view.show_graph(self.G, next_node)
                    except Exception as err:
                        print('Could not draw the graph:', err)
                current = next_node
        return steps
