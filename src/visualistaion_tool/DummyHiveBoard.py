import sys
import socket
import threading
import time

sys.path.insert(0, "../hiveboard")

from proto import message_pb2
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
        return None

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
                    break

                if msg.HasField("greeting"):
                    self.send_greet()

                elif msg.HasField("request"):
                    self.send_dummy_data()

    def send_greet(self):
        pass

    def send_dummy_data(self):
        pass



def main():
    dummy = DummyHiveBoard(55551)
    dummy.thread.start()
    dummy.thread.join()


if __name__ == "__main__":
    main()
