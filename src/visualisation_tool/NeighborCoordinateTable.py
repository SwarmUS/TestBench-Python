from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QThread, QObject
from threading import Lock
import PyQt5
import sys


class NeighborCoordinateTableWorker(QObject):

    def __init__(self, table):
        super().__init__()
        self.table = table

    def run(self):
        while True:
            self.table.check_neighbor_selection()
            QThread.msleep(500)


class NeighborCoordinateTable(QTableWidget):
    headers = ["Neighbor ID", "Name", "Distance", "Theta (degrees)", "Visible"]
    hide_neighbors = pyqtSignal(list)

    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.setWindowTitle("Neighbor List")
        self.neighbors = {}
        self.mutex = Lock()
        self.verticalHeader().setVisible(False)
        self.setHorizontalHeaderLabels(self.headers)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.cellChanged.connect(self.on_cell_changed)
        self.setMinimumWidth(int(self.width() / 2.2)) # Magic number to fix scaling
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.worker = NeighborCoordinateTableWorker(self)
        self.hiding_thread = QThread()
        self.worker.moveToThread(self.hiding_thread)
        self.hiding_thread.started.connect(self.worker.run)
        self.hiding_thread.start()

    # Allows modification by user only on the second column (Name)
    def edit(self, index, trigger, event):
        if index.column() != 1:
            trigger = self.NoEditTriggers
        return super().edit(index, trigger, event)

    @pyqtSlot(int, int)
    def on_cell_changed(self, _, __):
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setMinimumWidth(int(self.width()))

    @pyqtSlot(int, float, float)
    def update_neighbor(self, neighbor_id: int, distance: float, theta: float):
        self.mutex.acquire()
        if neighbor_id not in self.neighbors.keys():
            self.neighbors.update({neighbor_id: {"cell_id": QTableWidgetItem(str(neighbor_id)),
                                                 "cell_name": QTableWidgetItem(f"agent {neighbor_id}"),
                                                 "cell_distance": QTableWidgetItem("{:.2f}".format(distance)),
                                                 "cell_theta": QTableWidgetItem("{:.2f}".format(theta)),
                                                 "visible_check_box": QTableWidgetItem()}
                                   })
            checkable = self.neighbors[neighbor_id]["visible_check_box"]
            checkable.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkable.setCheckState(Qt.Checked)
            row = self.rowCount()
            column = 0
            self.setRowCount(row + 1)
            for cell in list(self.neighbors[neighbor_id].values()):
                self.setItem(row, column, cell)
                column += 1
            self.sortByColumn(0, Qt.AscendingOrder)
        else:
            self.neighbors[neighbor_id]["cell_distance"].setData(0, "{:.2f}".format(distance))
            self.neighbors[neighbor_id]["cell_theta"].setData(0, "{:.2f}".format(theta))
        self.mutex.release()

    @pyqtSlot()
    def clear_table(self):
        self.mutex.acquire()
        while self.rowCount() != 0:
            self.removeRow(0)
        self.neighbors.clear()
        self.mutex.release()

    def check_neighbor_selection(self):
        hidden_neighbors = []
        for neighbor in self.neighbors:
            current = self.neighbors[neighbor]["visible_check_box"]
            if current.checkState() != Qt.Checked:
                hidden_neighbors.append(int(self.neighbors[neighbor]["cell_id"].text()))

        self.hide_neighbors.emit(hidden_neighbors)


