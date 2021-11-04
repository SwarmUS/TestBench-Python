import threading
import time

from PyQt5.QtWidgets import *
from Graph2D import Graph2D
from PyQt5.QtCore import QThread, pyqtSlot
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np
from DataUpdater import DataUpdater


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.target_agent_id = None

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
            print(f"New target agent is {self.target_agent_id} based on configuration set")

    @pyqtSlot(int)
    def update_target_agent_from_greeting(self, agent_id):
        self.target_agent_id = agent_id
        for agent in self.checkable_agents:
            agent.setChecked(False)
        self.checkable_agents[agent_id-1].setChecked(True)
        print(f"New target agent is {self.target_agent_id} based on greeting received")



    def create_2d_graph_area(self):
        self.graphWidget = Graph2D(self)
        self.main_layout.addWidget(self.graphWidget)

    def start_data_acquisition(self):
        self.hiveboard = DataUpdater(self.graphWidget)
        self.hiveboard_thread = QThread()
        self.hiveboard.moveToThread(self.hiveboard_thread)
        self.hiveboard_thread.started.connect(self.hiveboard.generate_random_data)
        self.hiveboard_thread.start()







