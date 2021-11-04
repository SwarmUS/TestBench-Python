import sys
import socket
import threading
import time

sys.path.insert(0, "../hiveboard")

from proto.message_pb2 import Greeting, Message, InterlocState, UNSUPORTED, STANDBY, ANGLE_CALIB_RECEIVER
from proto.proto_stream import ProtoStream


class DummyHiveBoard(ProtoStream):

    def __init__(self, tcp_port: int):
        self.tcp_port = tcp_port
        self._run = True
        self.socket_connected = False

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.thread = threading.Thread(target=self.handle_inbound_messages())

    def __del__(self):
        self.socket.close()

    def kill_stream(self):
        self._run = False
        self.socket.close()

    def _read_from_stream(self,  num_bytes: int):
        data = self.socket.recv(num_bytes)
        while len(data) < num_bytes and self._run:
            print("Did not receive enough bytes")
            data += self.socket.recv(num_bytes-len(data))

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
        greet.agent_id = 1
        msg = Message()
        msg.greeting.CopyFrom(greet)
        msg.source_id = 1
        msg.destination_id = 1
        print("sending greet")
        self._write_to_stream(msg)

    def send_dummy_data(self):
        pass



def main():
    dummy = DummyHiveBoard(55551)
    dummy.thread.start()
    dummy.thread.join()


if __name__ == "__main__":
    main()
