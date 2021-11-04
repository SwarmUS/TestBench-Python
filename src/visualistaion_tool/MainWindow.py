import threading
import time

from PyQt5.QtWidgets import *
from Graph2D import Graph2D
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("SwarmUS Interlocalisation Visualisation Tool")


        # Call functions to add ui elements here
        self.graphWidget = Graph2D(self)
        self.setCentralWidget(self.graphWidget)
        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        config_menu = QMenu("&Configuration", self)
        menu_bar.addMenu(config_menu)

        clear_action = QAction("Clear", self)
        clear_action.setStatusTip("Update graph with test data")
        clear_action.triggered.connect(self.graphWidget.clear_points)
        menu_bar.addAction(clear_action)

        add_action = QAction("Add data", self)
        add_action.setStatusTip("Update graph with test data")
        add_action.triggered.connect(self.run)
        menu_bar.addAction(add_action)



    def run(self, e):
        n = 10
        pos = np.random.normal(size=(2, n), scale=1e-5)
        self.graphWidget.update_points(pos.transpose())




