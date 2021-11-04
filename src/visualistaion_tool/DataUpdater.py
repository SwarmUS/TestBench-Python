import time

from Graph2D import Graph2D
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import numpy as np
import sys

sys.path.insert(0, "../hiveboard")
from HiveBoard import HiveBoard
from usb_stream import UsbStream
from proto import message_pb2


class DataUpdater(QObject):

    new_points = pyqtSignal(list)

    def __init__(self, graph: Graph2D):
        super().__init__()
        self.graph = graph
        self.new_points.connect(self.graph.update_points_slot)

    def generate_random_data(self):
        while True:
            n = 10
            pos = np.random.normal(size=(2, n), scale=8)
            self.new_points.emit(pos.transpose().tolist())
            QThread.sleep(1)
