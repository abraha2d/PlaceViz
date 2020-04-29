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


class PlacementWindow(QMainWindow):
    def __init__(self, placement):
        super().__init__()

        self.placement = placement
        self.cellsWithoutLoc = []

        self.initializeWindow()
        self.initializePlot()

    def initializeWindow(self):
        self._main = QWidget()
        self.setCentralWidget(self._main)
        self.setWindowTitle(basename(self.placement.path))
        self.layout = QVBoxLayout(self._main)

    def initializePlot(self):
        static_canvas = FigureCanvas(Figure())
        self.layout.addWidget(static_canvas)
        self.addToolBar(NavigationToolbar(static_canvas, self))

        static_axes = static_canvas.figure.subplots()
        static_axes.set_aspect('equal')

        args = []
        for cell in self.placement.cells:
            try:
                x, y = cell.loc
                w, h = cell.width, cell.height
                xs = [x, x, x+w, x+w, x]
                ys = [y, y+h, y+h, y, y]
                args.extend([xs, ys, 'b'])
            except TypeError:
                self.cellsWithoutLoc.append(cell.id)
        static_axes.plot(*args, linewidth=0.5)

        args = []
        for net in self.placement.nets:
            for i in range(len(net.cells) - 1):
                start_cell = self.placement.cells[net.cells[i]-1].cloc
                end_cell = self.placement.cells[net.cells[i+1]-1].cloc
                xs = [start_cell[0], end_cell[0]]
                ys = [start_cell[1], end_cell[1]]
                args.extend([xs, ys, 'r'])
        static_axes.plot(*args, linewidth=0.25)

        if len(self.cellsWithoutLoc) > 0:
            QMessageBox.warning(
                None,
                "Warning",
                "The following cells did not have a placement:\n"
                f"\n{self.cellsWithoutLoc}",
            )
