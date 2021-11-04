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
        self.setWindowTitle("SwarmUS Interlocalisation Visualisation Tool")


        # Call functions to add ui elements here
        self.graphWidget = Graph2D(self)
        self.setCentralWidget(self.graphWidget)
        self.create_menu_bar()

        self.hiveboard = DataUpdater(self.graphWidget)
        self.hiveboard_thread = QThread()
        self.hiveboard.moveToThread(self.hiveboard_thread)
        self.hiveboard_thread.started.connect(self.hiveboard.generate_random_data)
        self.hiveboard_thread.start()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        config_menu = QMenu("&Configuration", self)
        menu_bar.addMenu(config_menu)





