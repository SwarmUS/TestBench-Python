import socket
from src.hiveboard.proto.proto_stream import ProtoStream


class EthernetStream(ProtoStream):
    def __init__(self, tcp_port: int):
        self._tcp_port = tcp_port
        self._run = True

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket: [socket, None] = None

    def __del__(self):
        super().__del__()

    def wait_connection(self):
        print(f'Starting socket on port {self._tcp_port}')
        print('Waiting for client connection')
        self.socket.bind(("0.0.0.0", self._tcp_port))
        self.socket.listen(1)
        self.client_socket, client_address = self.socket.accept()

        print(f'Connection from {client_address}')

    def kill_stream(self):
        self._run = False
        if self.client_socket is not None:
            self.client_socket.shutdown(socket.SHUT_WR)
            self.client_socket.close()
            self.client_socket = None

        self.socket.close()

    def _read_from_stream(self, num_bytes: int):
        data = self.client_socket.recv(num_bytes)
        while len(data) < num_bytes and self._run:
            data += self.client_socket.recv(num_bytes-len(data))

        if not self._run:
            return None

        return data

    def _write_to_stream(self, data: bytes):
        self.client_socket.send(data)


