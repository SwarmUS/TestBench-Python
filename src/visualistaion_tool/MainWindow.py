import threading
import time

from PyQt5.QtWidgets import *
from Graph2D import Graph2D
from PyQt5.QtCore import QThread, pyqtSlot, Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np
from NeighborCoordinateTable import NeighborCoordinateTable
from DataUpdater import DataUpdater


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.target_agent_id = None

        # Qt shenaninigans
        self.setWindowTitle("SwarmUS Interlocalisation Visualisation Tool")
        self.splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.splitter)

        # Create UI elements here
        self.create_2d_graph_area()
        self.create_menu_bar()
        self.create_neighbor_table()

        # Add backend elements here
        self.start_data_acquisition()
        self.data_updater.received_greeting.connect(self.update_target_agent_from_greeting)

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        config_menu = QMenu("&Configuration", self)
        target_agent_menu = QMenu("Target Agent", self)
        self.checkable_agents = []
        for i in range(1, 7):
            agent = QAction(f"Agent {i}", self)
            agent.setCheckable(True)
            target_agent_menu.addAction(agent)
            self.checkable_agents.append(agent)
            agent.triggered.connect(self.update_target_agent_from_config)
        config_menu.addMenu(target_agent_menu)
        menu_bar.addMenu(config_menu)

    @pyqtSlot(bool)
    def update_target_agent_from_config(self, checked: bool):
        if checked:
            checked_agents = [agent for agent in self.checkable_agents if agent.isChecked()]
            new_agent_id = 0
            for agent in checked_agents:
                if self.checkable_agents.index(agent) + 1 == self.target_agent_id:
                    agent.setChecked(False)
                else:
                    new_agent_id = self.checkable_agents.index(agent) + 1
            self.target_agent_id = new_agent_id
            self.data_updater.target_agent_id = self.target_agent_id
            self.data_updater.neighbor_list.clear()
            print(f"New target agent is {self.target_agent_id} based on configuration set")

    @pyqtSlot(int)
    def update_target_agent_from_greeting(self, agent_id):
        self.target_agent_id = agent_id
        for agent in self.checkable_agents:
            agent.setChecked(False)
        self.checkable_agents[agent_id - 1].setChecked(True)
        self.data_updater.target_agent_id = self.target_agent_id
        print(f"New target agent is {self.target_agent_id} based on greeting received")

    def create_2d_graph_area(self):
        self.graphWidget = Graph2D(self)
        self.splitter.addWidget(self.graphWidget)

    def create_neighbor_table(self):
        self.neighbor_table = NeighborCoordinateTable(0, 4)
        self.splitter.addWidget(self.neighbor_table)

    def start_data_acquisition(self):
        self.data_updater = DataUpdater(self.graphWidget, self.neighbor_table)
        self.data_updater_thread = QThread()
        self.data_updater.moveToThread(self.data_updater_thread)
        self.data_updater_thread.started.connect(self.data_updater.request_neighbors_update)
        self.data_updater_thread.start()
