from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from pyqtgraph import GridItem
import pyqtgraph as pg

COLOR_OFFSET = 15


class Graph2D(QtWidgets.QWidget):

    def __init__(self, parent):
        super(Graph2D, self).__init__(parent)
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.scatters = {}
        self.hidden_neighbors = []

        self.create_2d_plot()
        self.create_grid()
        self.create_scatter_element()

    def create_2d_plot(self):
        self.graphWidget = pg.plot()
        #self.graphWidget.setBackground("w")
        self.graphWidget.hideAxis('bottom')
        self.graphWidget.hideAxis('left')
        self.graphWidget.setXRange(-5, 5)
        self.graphWidget.setYRange(-5, 5)
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.graphWidget.addLegend(labelTextSize='24pt')
        self.layout.addWidget(self.graphWidget)

    def create_grid(self):
        self.grid = GridItem(pen='white', textPen='white')
        self.grid.setTickSpacing([1.0], [1.0])
        self.graphWidget.addItem(self.grid)

    def create_scatter_element(self):
        self.base = pg.ScatterPlotItem()
        base_symbol = {'pos': [0, 0],
                       'pen': {'color': 'w', 'width': 1},
                       'brush': pg.intColor(10, 100),  # Orange
                       'symbol': 'd',
                       'size': 50}
        self.base.addPoints([base_symbol])
        self.graphWidget.addItem(self.base)

    @pyqtSlot(int, float, float)
    def update_point(self, neighbor_id: int, x: float, y: float):
        if neighbor_id not in self.scatters.keys() and neighbor_id not in self.hidden_neighbors:
            self.scatters.update({neighbor_id: {"scatter": pg.ScatterPlotItem(name=f"agent {neighbor_id}",
                                                                              brush=pg.intColor(neighbor_id * COLOR_OFFSET, 100)),
                                                "spot": {}}})
            self.graphWidget.addItem(self.scatters[neighbor_id]["scatter"])
        if neighbor_id not in self.hidden_neighbors:
            self.scatters[neighbor_id]["spot"] = {'pos': [x, y],
                                                  'pen': {'color': 'w', 'width': 1},
                                                  # 100 is the number int values for the color spectrum,
                                                  # COLOR_OFFSET is the offset to apply to have 6 different values for points
                                                  'brush': pg.intColor(neighbor_id * COLOR_OFFSET, 100),
                                                  'size': 50}
            self.scatters[neighbor_id]["scatter"].setData(spots=[self.scatters[neighbor_id]["spot"]],
                                                          name=f"Agent {neighbor_id}")

    @pyqtSlot(list)
    def hide_neighbors(self, hidden_neighbors: list):
        self.hidden_neighbors = hidden_neighbors
        for neighbor_id in self.hidden_neighbors:
            if neighbor_id in self.scatters.keys():
                element = self.scatters.pop(neighbor_id)
                self.graphWidget.removeItem(element["scatter"])

