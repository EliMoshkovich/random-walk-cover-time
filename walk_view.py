"""Live visualization of the random walk."""

import matplotlib.pyplot as plt
import networkx as nx

IMAGE_FILE = 'random_walk_2d.png'


class WalkView:
    """Draws the state of the walk: blue = unvisited, red = visited, green = current."""

    def __init__(self, G):
        self.visited = set()
        self.pos = nx.spring_layout(G)  # fixed positions, so frames are comparable

    def mark_visited(self, node):
        """Record that the walk has stepped on `node`."""
        self.visited.add(node)

    def show_graph(self, G, current_node):
        """Draw the walk state, show it for two seconds, and save the frame to IMAGE_FILE."""
        colors = ['green' if node == current_node
                  else 'red' if node in self.visited
                  else 'blue'
                  for node in G.nodes()]
        fig, ax = plt.subplots()
        nx.draw(G, self.pos, ax=ax, node_color=colors, node_size=250, alpha=0.8, with_labels=True)
        ax.set_title('Random walk (green = current, red = visited, blue = unvisited)')
        plt.show(block=False)
        fig.savefig(IMAGE_FILE, dpi=150)
        plt.pause(2)
        plt.close(fig)
