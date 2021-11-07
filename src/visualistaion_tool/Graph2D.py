from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from pyqtgraph import PlotWidget, plot, GridItem
import pyqtgraph as pg

COLOR_OFFSET = 15


class Graph2D(QtWidgets.QWidget):

    def __init__(self, parent):
        super(Graph2D, self).__init__(parent)
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.points = {}

        self.create_2d_plot()
        self.create_grid()
        self.create_scatter_element()



    def create_2d_plot(self):
        self.graphWidget = pg.plot()
        self.graphWidget.setBackground("w")
        self.graphWidget.hideAxis('bottom')
        self.graphWidget.hideAxis('left')
        self.graphWidget.setXRange(-7, 7)
        self.graphWidget.setYRange(-7, 7)
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.layout.addWidget(self.graphWidget)

    def create_grid(self):
        self.grid = GridItem(pen='black', textPen='black')
        self.graphWidget.addItem(self.grid)

    def create_scatter_element(self):
        self.scatter = pg.ScatterPlotItem()
        self.base = pg.ScatterPlotItem()
        base_symbol = {'pos': [0, 0],
                       'pen': {'color': 'w', 'width': 1},
                       'brush': pg.intColor(10, 100),  # Orange
                       'symbol': 'd',
                       'size': 30}
        self.base.addPoints([base_symbol])
        self.graphWidget.addItem(self.base)
        self.graphWidget.addItem(self.scatter)


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
