from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
import PyQt5
import sys


class NeighborCoordinateTable(QTableWidget):
    data = {'col1': ['1', '2', '3', '4'],
            'col2': ['1', '2', '1', '3'],
            'col3': ['1', '1', '2', '1']}
    headers = ["Neighbor ID", "Name", "Distance", "Theta (degrees)"]

    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.neighbors = {}
        self.verticalHeader().setVisible(False)
        self.setData()
        self.setHorizontalHeaderLabels(self.headers)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.cellChanged.connect(self.on_cell_changed)

    # Allows modification by user only on the second column (Name)
    def edit(self, index, trigger, event):
        if index.column() != 1:
            trigger = self.NoEditTriggers
        return super().edit(index, trigger, event)

    def setData(self):
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(n, m, newitem)

    @pyqtSlot(int, int)
    def on_cell_changed(self, _, __):
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    @pyqtSlot(int, float, float)
    def update_neighbor(self, neighbor_id: int, distance: float, theta: float):
        if neighbor_id not in self.neighbors.keys():
            self.neighbors.update({neighbor_id: {"cell_id": QTableWidgetItem(neighbor_id),
                                                 "cell_name": QTableWidgetItem(f"agent {neighbor_id}"),
                                                 "cell_distance": QTableWidgetItem(distance),
                                                 "cell_theta": QTableWidgetItem(theta)}
                                   })
            row = self.rowCount()
            column = 0
            self.setRowCount(row + 1)
            for cell in list(self.neighbors[neighbor_id].values()):
                self.setItem(row, column, cell)
                column += 1
            self.sortByColumn(0, Qt.DescendingOrder)
        else:
            self.neighbors[neighbor_id]["cell_distance"].setData(distance)
            self.neighbors[neighbor_id]["cell_theta"].setData(theta)

