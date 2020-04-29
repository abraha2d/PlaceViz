# This Python file uses the following encoding: utf-8
from os.path import basename
import sys

from PySide2.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from matplotlib.backends.backend_qt5agg import (
    FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

from loaders import get_placement_details


class PlacementWindow(QMainWindow):
    def __init__(self, placement, app):
        super().__init__()
        self.app = app

        self.placement = placement
        self.cellsWithoutLoc = []

        self.initializeWindow()
        self.initializePlot()

    def initializeWindow(self):
        self._main = QWidget()
        self.setCentralWidget(self._main)
        self.setWindowTitle(get_placement_details(self.placement.csvPath))
        self.layout = QVBoxLayout(self._main)

    def initializePlot(self):
        self.canvas = FigureCanvas(Figure())
        self.layout.addWidget(self.canvas)
        self.addToolBar(NavigationToolbar(self.canvas, self))
        self.pw = self.canvas.figure.subplots()
        self.pw.set_aspect('equal')

    def plot(self):
        args1 = []
        for cell in self.placement.cells:
            try:
                self.app.processEvents()
                x, y = cell.loc
                w, h = cell.width, cell.height
                xs = [x, x, x+w, x+w, x]
                ys = [y, y+h, y+h, y, y]
                args1.extend([xs, ys, 'b'])
            except TypeError:
                self.cellsWithoutLoc.append(cell.id)

        self.pw.plot(*args1, linewidth=0.5)
        self.canvas.draw()
        self.app.processEvents()

        args2 = []
        for net in self.placement.nets:
            g = Graph(net, self.placement.cells)
            edges = g.primMST()
            for edge, weight in edges:
                if weight > self.placement.core.width / 2:
                    self.app.processEvents()
                    if (
                        g.cells[edge[0]] in self.cellsWithoutLoc or
                        g.cells[edge[1]] in self.cellsWithoutLoc
                    ):
                        continue
                    start_cell = self.placement.cells[g.cells[edge[0]]-1].cloc
                    end_cell = self.placement.cells[g.cells[edge[1]]-1].cloc
                    xs = [start_cell[0], end_cell[0]]
                    ys = [start_cell[1], end_cell[1]]
                    args2.extend([xs, ys, 'r'])

        self.pw.plot(*args2, linewidth=0.25)
        self.canvas.draw()
        self.app.processEvents()

        core = self.placement.core
        w, h = core.width, core.height
        xs = [0, 0, w, w, 0]
        ys = [0, h, h, 0, 0]
        self.pw.plot(xs, ys, 'c', linewidth=0.5)
        self.canvas.draw()
        self.app.processEvents()

        mh, mv = core.c2i_h, core.c2i_v
        xs = [-mh, -mh, w+mh, w+mh, -mh]
        ys = [-mv, h+mv, h+mv, -mv, -mv]
        self.pw.plot(xs, ys, 'c', linewidth=0.5)
        self.canvas.draw()
        self.app.processEvents()

        if len(self.cellsWithoutLoc) > 0:
            QMessageBox.warning(
                None,
                f"{basename(self.placement.path)}",
                "The following cells did not have a placement:\n"
                f"\n{self.cellsWithoutLoc}",
            )


# Adapted from the following link:
# https://www.geeksforgeeks.org/prims-minimum-spanning-tree-mst-greedy-algo-5/
class Graph():

    def __init__(self, net, cells):
        self.V = len(net.cells)
        self.graph = [[0 for column in range(self.V)]
                      for row in range(self.V)]
        self.cells = []
        for i in range(self.V):
            self.cells.append(net.cells[i])
            for j in range(self.V):
                self.graph[i][j] = self.getCellDist(
                    cells[net.cells[i]-1],
                    cells[net.cells[j]-1],
                )

    @staticmethod
    def getCellDist(cell1, cell2):
        try:
            x1, y1 = cell1.cloc
            x2, y2 = cell2.cloc
        except TypeError:
            return sys.maxsize - 1
        return ((y2-y1)**2+(x2-x1)**2)**0.5

    # A utility function to return the edges of the MST stored in parent[]
    def returnEdges(self, parent):
        edges = []
        for i in range(1, self.V):
            edges.append(((parent[i], i), self.graph[i][parent[i]]))
        return edges

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minKey(self, key, mstSet):
        min = sys.maxsize

        for v in range(self.V):
            if key[v] < min and not mstSet[v]:
                min = key[v]
                min_index = v

        return min_index

    # Function to construct and print MST for a graph
    # represented using adjacency matrix representation
    def primMST(self):

        # Key values used to pick minimum weight edge in cut
        key = [sys.maxsize] * self.V
        parent = [None] * self.V  # Array to store constructed MST
        # Make key 0 so that this vertex is picked as first vertex
        key[0] = 0
        mstSet = [False] * self.V

        parent[0] = -1  # First node is always the root of

        for cout in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minKey(key, mstSet)

            # Put the minimum distance vertex in
            # the shortest path tree
            mstSet[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shotest path tree
            for v in range(self.V):
                # graph[u][v] is non zero only for adjacent vertices of m
                # mstSet[v] is false for vertices not yet included in MST
                # Update the key only if graph[u][v] is smaller than key[v]
                if (
                    self.graph[u][v] > 0 and
                    not mstSet[v] and
                    key[v] > self.graph[u][v]
                ):
                    key[v] = self.graph[u][v]
                    parent[v] = u

        return self.returnEdges(parent)
