# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtCore import QUrl
from PySide2.QtGui import QIcon
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("PlaceViz")
    app.setWindowIcon(QIcon("icon.png"))

    view = QQuickView()
    view.setSource(QUrl("main.qml"))
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.show()

    sys.exit(app.exec_())
