import serial

from src.hiveboard.proto.proto_stream import ProtoStream


class UsbStream(ProtoStream):
    def __init__(self, serial_port: str):
        self._serial_port = serial_port
        self._serial = serial.Serial(
            port=serial_port
        )

    def read_from_stream(self, num_bytes: int):
        return self._serial.read(num_bytes)

    def write_to_stream(self, data: bytes):
        self._serial.write(data)
