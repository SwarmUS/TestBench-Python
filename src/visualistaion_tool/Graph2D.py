from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np



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
                'brush': pg.intColor(10, 100),
                'symbol': 'd',
                'size': 30}
        self.base.addPoints([base_symbol])
        self.graphWidget.addItem(self.base)
        self.graphWidget.addItem(self.scatter)
        self.layout.addWidget(self.graphWidget)

    def update_points(self, points: list):
        self.scatter.clear()
        spots = []
        for i in range(len(points)):
            spot = {'pos': points[i],
                    'pen': {'color': 'w', 'width': 1},
                    'brush': pg.intColor(i * 10, 100)}
            spots.append(spot)
            i += 1
        self.scatter.setData(spots)

    @pyqtSlot(list)
    def update_points_slot(self, points: list):
        self.update_points(points)

    @pyqtSlot(int, float, float)
    def update_point(self, neighbor_id: int, x: float, y: float):
        self.points[neighbor_id] = {'pos': [x, y],
                                    'pen': {'color': 'w', 'width': 1},
                                    'brush': pg.intColor(neighbor_id * 15, 100),
                                    'size': 20}
        self.scatter.clear()
        self.scatter.setData(list(self.points.values()))


