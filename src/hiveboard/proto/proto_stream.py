from abc import ABC, abstractmethod
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes

from src.hiveboard.proto.message_pb2 import Message


class ProtoStream(ABC):
    def read_message_from_stream(self) -> [Message, None]:
        data = self._read_delimited_from_stream()

        if data is None:
            return None

        msg = Message()
        msg.ParseFromString(data)

        return msg

    def write_message_to_stream(self, msg: Message):
        message_bytes = _VarintBytes(msg.ByteSize()) + msg.SerializeToString()
        self._write_to_stream(message_bytes)

    @abstractmethod
    def kill_stream(self):
        pass

    def _read_delimited_from_stream(self) -> [bytes, None]:
        data = self._read_from_stream(4)

        if data is None or len(data) == 0:
            return None

        msg_len, new_pos = _DecodeVarint32(data, 0)
        nb_to_read = msg_len - (4 - new_pos)
        data = data[new_pos:] + self._read_from_stream(nb_to_read)

        return data

    @abstractmethod
    def _read_from_stream(self, num_bytes: int) -> bytes:
        pass

    @abstractmethod
    def _write_to_stream(self, data: bytes):
        pass

