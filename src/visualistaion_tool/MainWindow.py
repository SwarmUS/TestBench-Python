import threading
import time

from PyQt5.QtWidgets import *
from Graph2D import Graph2D
from PyQt5.QtCore import QThread
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np
from DataUpdater import DataUpdater


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        #Qt shenaninigans
        self.setWindowTitle("SwarmUS Interlocalisation Visualisation Tool")
        self.container = QWidget()
        self.main_layout = QVBoxLayout()
        self.container.setLayout(self.main_layout)
        self.setCentralWidget(self.container)

        # Create UI elements here
        self.create_2d_graph_area()
        self.create_menu_bar()

        # Add backend elements here
        self.start_data_acquisition()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        config_menu = QMenu("&Configuration", self)
        menu_bar.addMenu(config_menu)

    def create_2d_graph_area(self):
        self.graphWidget = Graph2D(self)
        self.main_layout.addWidget(self.graphWidget)

    def start_data_acquisition(self):
        self.hiveboard = DataUpdater(self.graphWidget)
        self.hiveboard_thread = QThread()
        self.hiveboard.moveToThread(self.hiveboard_thread)
        self.hiveboard_thread.started.connect(self.hiveboard.generate_random_data)
        self.hiveboard_thread.start()







