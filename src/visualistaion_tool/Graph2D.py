from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np


class Graph2D(QtWidgets.QWidget):

    def __init__(self, parent):
        super(Graph2D, self).__init__(parent)
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.graphWidget = pg.plot()
        self.graphWidget.setXRange(-15, 15)
        self.graphWidget.setYRange(-15, 15)
        self.scatter = pg.ScatterPlotItem(size=10)
        self.base = pg.ScatterPlotItem(size=10)
        base_symbol = {'pos': [0,0],
                'pen': {'color': 'w', 'width': 1},
                'brush': pg.intColor(10, 100),
                'symbol': 'd',
                'size': 30}
        self.base.addPoints([base_symbol])
        self.graphWidget.addItem(self.base)

        n = 10
        pos = np.random.normal(size=(2, n), scale=1)

        # creating spots using the random position
        spots_1 = [{'pos': pos[:, i], 'data': i}
                 for i in range(n)] + [{'pos': [0, 0], 'data': 1}]

        self.update_points(pos.transpose())
        #self.scatter.addPoints(spots_1)
        self.graphWidget.addItem(self.scatter)
        self.layout.addWidget(self.graphWidget)

    def update_points(self, points: list):
        self.clear_points()
        i = 0
        spots = []
        for i in range(len(points)):
            spot = {'pos': points[i],
                    'pen': {'color': 'w', 'width': 1},
                    'brush': pg.intColor(i * 10, 100)}
            spots.append(spot)
            i += 1
        self.scatter.setData(spots)
        self.graphWidget.addItem(self.scatter)

    def clear_points(self):
        self.graphWidget.removeItem(self.scatter)
        self.scatter.clear()
