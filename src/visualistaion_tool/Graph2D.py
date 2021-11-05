from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np

COLOR_OFFSET = 15

class Graph2D(QtWidgets.QWidget):

    def __init__(self, parent):
        super(Graph2D, self).__init__(parent)
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.points = {}

        self.graphWidget = pg.plot()
        self.graphWidget.setXRange(-15, 15)
        self.graphWidget.setYRange(-15, 15)
        self.scatter = pg.ScatterPlotItem()
        self.base = pg.ScatterPlotItem()
        base_symbol = {'pos': [0,0],
                'pen': {'color': 'w', 'width': 1},
                'brush': pg.intColor(10, 100), # Orange
                'symbol': 'd',
                'size': 30}
        self.base.addPoints([base_symbol])
        self.graphWidget.addItem(self.base)
        self.graphWidget.addItem(self.scatter)
        self.layout.addWidget(self.graphWidget)

    @pyqtSlot(int, float, float)
    def update_point(self, neighbor_id: int, x: float, y: float):
        self.points[neighbor_id] = {'pos': [x, y],
                                    'pen': {'color': 'w', 'width': 1},
                                    # 100 is the number int values for the color spectrum,
                                    # COLOR_OFFSET is the offset to apply to have 6 different values for points
                                    'brush': pg.intColor(neighbor_id * COLOR_OFFSET, 100),
                                    'size': 20}
        self.scatter.clear()
        self.scatter.setData(list(self.points.values()))


