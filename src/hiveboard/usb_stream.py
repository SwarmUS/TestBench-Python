import serial

from src.hiveboard.proto.proto_stream import ProtoStream


class UsbStream(ProtoStream):
    def __init__(self, serial_port: str):
        self._serial_port = serial_port
        self._run = True
        self._serial = serial.Serial(
            port=serial_port,
            timeout=1,
        )

    def kill_stream(self):
        self._run = False
        self._serial.close()
        self._serial.cancel_read()
        self._serial.cancel_write()

    def _read_from_stream(self, num_bytes: int):
        data = self._serial.read(num_bytes)
        while (data is None or len(data) == 0) and self._run:
            data = self._serial.read(num_bytes)

        return data

    def _write_to_stream(self, data: bytes):
        self._serial.write(data)


