# This Python file uses the following encoding: utf-8
from os.path import basename

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

#import pyqtgraph as pg


class PlacementWindow(QMainWindow):
    def __init__(self, placement, app):
        super().__init__()
        self.app = app

        self.placement = placement
        self.cellsWithoutLoc = []

        self.initializeWindow()
        self.initializeMatPlot()

    def initializeWindow(self):
        self._main = QWidget()
        self.setCentralWidget(self._main)
        self.setWindowTitle(basename(self.placement.path))
        self.layout = QVBoxLayout(self._main)

#    def initializePlot(self):
#        self.pw = pg.PlotWidget(self._main)
#        self.layout.addWidget(self.pw)

    def initializeMatPlot(self):
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
            for i in range(len(net.cells) - 1):
                self.app.processEvents()
                start_cell = self.placement.cells[net.cells[i]-1].cloc
                end_cell = self.placement.cells[net.cells[i+1]-1].cloc
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
                "Warning",
                "The following cells did not have a placement:\n"
                f"\n{self.cellsWithoutLoc}",
            )
