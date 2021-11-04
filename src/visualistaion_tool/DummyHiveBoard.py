import random
import sys
import socket
import threading
import time
import numpy as np

sys.path.insert(0, "../hiveboard")

from proto.message_pb2 import Greeting, Message, InterlocState, UNSUPORTED, STANDBY, ANGLE_CALIB_RECEIVER
from src.hiveboard.proto.message_pb2 import GetNeighborsListResponse, HiveMindHostApiResponse, Response, GetNeighborResponse, NeighborPosition
from src.hiveboard.proto.message_pb2 import GetNeighborsListRequest, GetNeighborRequest, HiveMindHostApiRequest, Request
from proto.proto_stream import ProtoStream


class DummyHiveBoard(ProtoStream):

    def __init__(self, tcp_port: int):
        self.tcp_port = tcp_port
        self._run = True
        self.socket_connected = False
        self.uuid = 1

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.thread = threading.Thread(target=self.handle_inbound_messages())

        self.agent_list = [2, 3, 4, 5, 6]

    def __del__(self):
        self.socket.close()

    def kill_stream(self):
        self._run = False
        self.socket.close()

    def _read_from_stream(self, num_bytes: int):
        data = self.socket.recv(num_bytes)
        while len(data) < num_bytes and self._run:
            print("Did not receive enough bytes")
            data += self.socket.recv(num_bytes - len(data))

        if not self._run:
            return None

        return data

    def _write_to_stream(self, data: bytes):
        self.socket.send(data)

    def handle_inbound_messages(self):
        while True:
            if not self.socket_connected:
                try:
                    self.socket.connect(("127.0.0.1", self.tcp_port))
                    self.socket_connected = True
                except:
                    print("Dummy HiveBoard trying to connect to app")
                    time.sleep(1)
            else:
                msg = self.read_message_from_stream()

                if msg is None:
                    continue

                if msg.HasField("greeting"):
                    self.send_greet()

                elif msg.HasField("request"):
                    self.send_dummy_data()

    def send_greet(self):
        greet = Greeting()
        greet.agent_id = self.uuid
        msg = Message()
        msg.greeting.CopyFrom(greet)
        msg.source_id = self.uuid
        msg.destination_id = self.uui
        self.write_message_to_stream(msg)

    def handle_requests(self, request: Request):
        if request.HasField("hivemind_host"):
            hivemind_host_api = request.hivemind_host
            if hivemind_host_api.HasField("neighbors_list"):
                self.send_neighbor_list()
            elif hivemind_host_api.HasField("neighbor"):
                self.send_neighbor_position(hivemind_host_api.neighbor)
        pass

    def send_neighbor_list(self):
        neighbor_list = GetNeighborsListResponse()
        neighbor_list.neighbors = self.agent_list

        api_response = HiveMindHostApiResponse()
        api_response.neighbors_list.CopyFrom(neighbor_list)

        response = Response()
        response.hivemind_host.CopyFrom(api_response)

        msg = Message()
        msg.source_id = self.uuid
        msg.destination_id = self.uuid
        msg.response.CopyFrom(response)
        self._write_to_stream(msg)

    def send_neighbor_position(self, neighbor):
        neighbor_position = NeighborPosition()
        neighbor_position.distance = random.random() * 10 # All positions will be within 8 meters of center
        neighbor_position.azimuth = random.random() * 2 * np.pi # Angle between 0 and 2pi
        neighbor_position.in_los = True

        neighbor_response = GetNeighborResponse()
        neighbor_response.neighbor_id = neighbor.neighbor_id
        neighbor_response.position.CopyFrom(neighbor_position)

        hivemind_api_response = HiveMindHostApiResponse()
        hivemind_api_response.neighbor.CopyFrom(neighbor_response)

        response = Response()
        response.hivemind_host.CopyFrom(hivemind_api_response)

        msg = Message()
        msg.source_id = self.uuid
        msg.destination_id = self.uuid
        msg.response.CopyFrom(response)
        self._write_to_stream(msg)



def main():
    dummy = DummyHiveBoard(55551)
    dummy.thread.start()
    dummy.thread.join()


if __name__ == "__main__":
    main()
