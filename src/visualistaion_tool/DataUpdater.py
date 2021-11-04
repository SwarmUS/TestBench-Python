import threading
import time

from Graph2D import Graph2D
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import numpy as np
import sys

sys.path.insert(0, "../hiveboard")
from HiveBoard import HiveBoard
from usb_stream import UsbStream
from proto import message_pb2
from proto.ethernet_stream import EthernetStream

use_serial = False
COM_PORT = "/dev/ttyUSB0"


class DataUpdater(QObject):
    new_points = pyqtSignal(list)
    received_greeting = pyqtSignal(int)

    def __init__(self, graph: Graph2D):
        super().__init__()

        self.graph = graph
        self.new_points.connect(self.graph.update_points_slot)
        self.hiveboard = None
        self.hiveboard_connnected = False
        self.target_agent_id = 0

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

    def send_greet_message(self):
        while self.hiveboard.uuid == 0:
            self.hiveboard.greet()
            time.sleep(2)

    def generate_random_data(self):
        while True:
            if self.hiveboard.uuid != 0 and self.target_agent_id != 0:
                n = 10
                pos = np.random.normal(size=(2, n), scale=8)
                self.new_points.emit(pos.transpose().tolist())
                time.sleep(0.1)
