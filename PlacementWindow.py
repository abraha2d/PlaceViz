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
        for cell in self.placement.cells:
            try:
                x, y = cell.loc
                w, h = cell.width, cell.height
                xs = [x, x, x+w, x+w, x]
                ys = [y, y+h, y+h, y, y]
                static_axes.plot(xs, ys, color='blue', linewidth=0.5)
            except TypeError:
                self.cellsWithoutLoc.append(cell.id)

        if len(self.cellsWithoutLoc) > 0:
            QMessageBox.warning(
                None,
                "Warning",
                "The following cells did not have a placement:\n"
                f"\n{self.cellsWithoutLoc}",
            )
