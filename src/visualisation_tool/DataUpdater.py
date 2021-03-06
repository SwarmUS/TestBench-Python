import threading
import time

from src.visualisation_tool.Graph2D import Graph2D
from src.visualisation_tool.NeighborCoordinateTable import NeighborCoordinateTable
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np
import sys

from src.hiveboard.HiveBoard import HiveBoard
from src.hiveboard.usb_stream import UsbStream
from src.hiveboard.proto.ethernet_stream import EthernetStream

use_serial = True
COM_PORT = "/dev/ttyACM0"


class DataUpdater(QObject):
    new_cartesian_point = pyqtSignal(int, float, float)
    new_polar_point = pyqtSignal(int, float, float)
    received_greeting = pyqtSignal(int)

    def __init__(self, graph: Graph2D, table: NeighborCoordinateTable):
        super().__init__()

        self.graph = graph
        self.neighbor_table = table
        self.new_cartesian_point.connect(self.graph.update_point)
        self.new_polar_point.connect(self.neighbor_table.update_neighbor)
        self.hiveboard = None
        self.hiveboard_connnected = False
        self.target_agent_id = 0

        self.neighbor_list = []
        self.neighbor_table.hide_neighbors.connect(self.graph.hide_neighbors)

        self.start_connection_thread()
        self.start_greeting_thread()

    def start_connection_thread(self):
        self.active_thread = threading.Thread(target=self.wait_for_connection)
        self.active_thread.start()

    def start_greeting_thread(self):
        self.active_thread.join()
        self.active_thread = threading.Thread(target=self.send_greet_message)
        self.active_thread.start()

    def wait_for_connection(self):
        while not self.hiveboard_connnected:
            if use_serial:
                try:
                    self.hiveboard = HiveBoard(UsbStream(COM_PORT))
                    self.hiveboard_connnected = True
                except:
                    print(f"Could not open serial port {COM_PORT}")
                    time.sleep(1)
            else:
                self.tcp_stream = EthernetStream(55551)
                print("Waiting for hiveboard connection ...")
                self.tcp_stream.wait_connection()
                self.hiveboard = HiveBoard(self.tcp_stream)
                self.hiveboard_connnected = True
        self.hiveboard.set_neighbor_list_callback(callback=self.handle_neighbor_list)
        self.hiveboard.set_neighbor_position_callback(callback=self.handle_neigbor_update)

    def send_greet_message(self):
        while self.hiveboard.uuid == 0:
            self.hiveboard.greet()
            time.sleep(2)
        self.received_greeting.emit(self.hiveboard.uuid)

    def refresh_neighbor_list(self):
        self.hiveboard.send_get_neighbors_request(self.target_agent_id)

    def handle_neighbor_list(self, neighbor_list):
        self.neighbor_list = neighbor_list
        print(f"New neighbor list is {self.neighbor_list}")

    def handle_neigbor_update(self, neighbor):
        neighbor_id = neighbor.neighbor_id
        self.new_polar_point.emit(neighbor_id, neighbor.position.distance, neighbor.position.azimuth)
        y = -neighbor.position.distance * np.cos(neighbor.position.azimuth / 180 * np.pi)
        x = neighbor.position.distance * np.sin(neighbor.position.azimuth / 180 * np.pi)
        self.new_cartesian_point.emit(neighbor_id, x, y)

    def request_neighbors_update(self):
        while True:
            if self.hiveboard.uuid != 0 and self.target_agent_id != 0:

                if len(self.neighbor_list) == 0:
                    self.refresh_neighbor_list()

                for neighbor_id in self.neighbor_list:
                    self.hiveboard.send_get_neighbor_position_request(destination=self.target_agent_id,
                                                                      neighbor_id=neighbor_id)
            time.sleep(0.2)
