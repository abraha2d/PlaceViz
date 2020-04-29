# This Python file uses the following encoding: utf-8
import sys
import time

import numpy as np

from PySide2.QtCore import Qt

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
        self._main = QWidget()
        self.setCentralWidget(self._main)
        layout = QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(static_canvas)
        self.addToolBar(NavigationToolbar(static_canvas, self))

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

