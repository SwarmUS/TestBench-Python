from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys




class NeighborCoordinateTable(QTableWidget):
    data = {'col1': ['1', '2', '3', '4'],
            'col2': ['1', '2', '1', '3'],
            'col3': ['1', '1', '2', '1']}

    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setData(self):
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)
