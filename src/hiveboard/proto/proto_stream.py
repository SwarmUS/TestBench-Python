from abc import ABC, abstractmethod
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes

from src.hiveboard.proto.message_pb2 import Message


class ProtoStream(ABC):
    @abstractmethod
    def read_from_stream(self, num_bytes: int) -> bytes:
        pass

    @abstractmethod
    def write_to_stream(self, data: bytes):
        pass

    def read_message_from_stream(self) -> Message:
        data = self._read_delimited_from_stream()
        msg = Message()
        msg.ParseFromString(data)

        return msg

    def write_message_to_stream(self, msg: Message):
        message_bytes = _VarintBytes(msg.ByteSize()) + msg.SerializeToString()
        self.write_to_stream(message_bytes)

    def _read_delimited_from_stream(self) -> bytes:
        data = self.read_from_stream(4)
        msg_len, new_pos = _DecodeVarint32(data, 0)
        nb_to_read = msg_len - (4 - new_pos)
        data = data[new_pos:] + self.read_from_stream(nb_to_read)

        return data
