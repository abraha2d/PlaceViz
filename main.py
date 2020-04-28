# This Python file uses the following encoding: utf-8
from os.path import basename
import sys

from PySide2.QtCore import (
    Property,
    QAbstractListModel,
    QModelIndex,
    QObject,
    QTimer,
    QUrl,
    Signal,
    Slot,
)
from PySide2.QtGui import QIcon
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMessageBox,
)

from loaders import get_benchmarks, load_data


class BenchmarkWrapper(QObject):
    def __init__(self, benchmark):
        super().__init__()
        self._benchmark = benchmark

    def _name(self):
        return self._benchmark['name']
    name_changed = Signal()
    name = Property("QString", _name, notify=name_changed)

    def _path(self):
        return self._benchmark['path']
    path_changed = Signal()
    path = Property("QString", _path, notify=path_changed)

    def _isPlaced(self):
        return self._benchmark['isPlaced']
    isPlaced_changed = Signal()
    isPlaced = Property("bool", _isPlaced, notify=isPlaced_changed)

    def _isOther(self):
        return self._benchmark.get('isOther', False)
    isOther_changed = Signal()
    isOther = Property("bool", _isOther, notify=isOther_changed)


class BenchmarkListModel(QAbstractListModel):
    def __init__(self, benchmarks):
        super().__init__()
        self._benchmarks = benchmarks

    def rowCount(self, parent=QModelIndex()):
        return len(self._benchmarks) + 1

    def data(self, index, role):
        if index.row() == len(self._benchmarks):
            return BenchmarkWrapper({
                'name': "Benchmark not listed?",
                'path': "Click to select a benchmark...",
                'isOther': True,
            })
        return self._benchmarks[index.row()]

    def roleNames(self):
        return {0: b'benchmark'}


class Controller(QObject):
    @Slot(QObject)
    def benchmarkClicked(self, wrapper):
        if wrapper._benchmark.get('isOther', False):
            print("Opening dialog for user to select benchmark...")
            path = QFileDialog.getOpenFileName(
                None,
                "Open benchmark",
                "benchmarks/",
                "Benchmark files (*.hgr)"
            )[0]
        else:
            path = wrapper._benchmark['path']

        if path:
            result = load_data(path)

            if result[0] == -1:
                QMessageBox.critical(
                    None,
                    f"{basename(path)}",
                    f"Could not load benchmark.\n\nReason: {result[1]}",
                )

            elif result[0] == -2:
                run_placement = QMessageBox.question(
                    None,
                    f"{basename(path)}",
                    "This benchmark has not been placed yet.\n\nWould you like to run placement?",
                )

                if run_placement == QMessageBox.StandardButton.Yes:
                    # TODO: Run placement
                    QMessageBox.critical(
                        None,
                        "Error",
                        "This function has not been implemented yet.",
                    )

            else:
                print(result[1])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("PlaceViz")
    app.setWindowIcon(QIcon("icon.png"))

    engine = QQmlApplicationEngine()
    rootContext = engine.rootContext()

    controller = Controller()
    rootContext.setContextProperty("controller", controller)

    benchmarks = [BenchmarkWrapper(b) for b in get_benchmarks()]
    benchmarkList = BenchmarkListModel(benchmarks)
    rootContext.setContextProperty("benchmarkList", benchmarkList)

    engine.load(QUrl("qml/main.qml"))

    sys.exit(app.exec_())
