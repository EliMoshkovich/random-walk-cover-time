"""Tkinter front end: build a graph, then run a random walk on it."""

import tkinter as tk
from tkinter import messagebox

import networkx as nx

from graph_builder import GraphBuilder
from random_walk import RandomWalk

ABOUT_TEXT = (
    'Random Walks — a cover time explorer.\n\n'
    'Build a random regular graph, a G(n, m) random graph, or a random tree, '
    'then choose File → Run Random Walk. A simple random walk runs on the last '
    'built graph until every node has been visited, and the pop-up at the end '
    'reports the cover time.'
)


class GUI:
    """The main window: graph parameters, build buttons, and the walk menu."""

    def __init__(self, root, builder):
        self.root = root
        self.builder = builder
        root.title('Random Walk')
        root.resizable(width=False, height=False)
        root.geometry('400x250+600+300')

        menu = tk.Menu(root)
        root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label='Run Random Walk', command=self.run_walk)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=root.quit)
        menu.add_cascade(label='File', menu=file_menu)
        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label='About', command=self.about)
        menu.add_cascade(label='Help', menu=help_menu)

        title = tk.Label(root, text='Choose a graph to build:')
        title.config(font=('Courier', 14))
        title.pack()

        tk.Label(root, text='Nodes').pack(fill=tk.X)
        self.nodes_entry = tk.Entry(root)
        self.nodes_entry.pack()
        tk.Label(root, text='Edges (degree, for a regular graph)').pack(fill=tk.X)
        self.edges_entry = tk.Entry(root)
        self.edges_entry.pack()

        self.show_walk = tk.IntVar()
        tk.Checkbutton(root, text='Show the walk', variable=self.show_walk).pack()

        tk.Button(root, text='Regular Graph', command=self.build_regular).pack(fill='none', expand=True)
        tk.Button(root, text='Random Graph', command=self.build_random).pack(fill='none', expand=True)
        tk.Button(root, text='Tree Graph', command=self.build_tree).pack(fill='none', expand=True)

    def run_walk(self):
        """Load the last saved graph and run a random walk on it until it is covered."""
        try:
            walk = RandomWalk()
        except FileNotFoundError:
            messagebox.showerror('Error!', 'No saved graph found. Please build a graph first.')
            return
        try:
            steps = walk.run(self.show_walk.get())
        except ValueError as err:
            messagebox.showerror('Error!', str(err))
            return
        messagebox.showinfo('Covered!', f'Cover time: {steps} steps\n'
                                        f'Nodes: {walk.G.number_of_nodes()}\n'
                                        f'Edges: {walk.G.number_of_edges()}\n'
                                        f'Density: {nx.density(walk.G):.4f}')

    def about(self):
        """Show the About pop-up."""
        messagebox.showinfo('About', ABOUT_TEXT)

    def build_tree(self):
        """Build a uniformly random tree with the requested number of nodes."""
        try:
            v = int(self.nodes_entry.get())
        except ValueError:
            messagebox.showerror('Error!', 'Please insert an integer number of nodes!')
            return
        if v < 1:
            messagebox.showerror('Error!', 'Please insert a positive number of nodes!')
            return
        self.builder.v = v
        self.builder.tree_graph()

    def build_regular(self):
        """Build a random d-regular graph after validating the parameters."""
        params = self._read_parameters()
        if params is None:
            return
        v, d = params
        if v * d % 2 != 0:
            messagebox.showerror('Error!', 'In a regular graph, nodes × degree must be even!')
        elif d >= v:
            messagebox.showerror('Error!', 'The degree must be smaller than the number of nodes!')
        else:
            self.builder.v, self.builder.e = v, d
            self.builder.regular_graph()

    def build_random(self):
        """Build a G(n, m) random graph after validating the parameters."""
        params = self._read_parameters()
        if params is None:
            return
        self.builder.v, self.builder.e = params
        self.builder.random_graph()

    def _read_parameters(self):
        """Parse and validate both entry fields; return (nodes, edges) or None."""
        try:
            v = int(self.nodes_entry.get())
            e = int(self.edges_entry.get())
        except ValueError:
            messagebox.showerror('Error!', 'Please insert two integers!')
            return None
        if v < 1 or e < 0:
            messagebox.showerror('Error!', 'The number of nodes must be positive '
                                           'and the second field non-negative!')
            return None
        return v, e


if __name__ == '__main__':
    tk_root = tk.Tk()
    GUI(tk_root, GraphBuilder())
    tk_root.mainloop()
