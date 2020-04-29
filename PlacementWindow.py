# This Python file uses the following encoding: utf-8
import numpy as np
from os.path import basename

from PySide2.QtWidgets import (
    QMainWindow,
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

        t = np.linspace(0, 10, 501)
        static_axes = static_canvas.figure.subplots()
        static_axes.plot(t, np.tan(t), ".")

