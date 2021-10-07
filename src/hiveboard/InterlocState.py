from abc import ABC, abstractmethod

from hiveboard.proto.message_pb2 import STANDBY, OPERATING, ANGLE_CALIB_SENDER, ANGLE_CALIB_RECEIVER, \
    TWR_CALIB_INITIATOR, TWR_CALIB_RESPONDER


class InterlocState(ABC):
    @abstractmethod
    def to_proto(self):
        pass


class InterlocState_STANDBY(InterlocState):
    def to_proto(self):
        return STANDBY


class InterlocState_OPERATING(InterlocState):
    def to_proto(self):
        return OPERATING


class InterlocState_ANGLE_CALIB_SENDER(InterlocState):
    def to_proto(self):
        return ANGLE_CALIB_SENDER


class InterlocState_ANGLE_CALIB_RECEIVER(InterlocState):
    def to_proto(self):
        return ANGLE_CALIB_RECEIVER


class InterlocState_TWR_CALIB_INITIATOR(InterlocState):
    def to_proto(self):
        return TWR_CALIB_INITIATOR


class InterlocState_TWR_CALIB_RESPONDER(InterlocState):
    def to_proto(self):
        return TWR_CALIB_RESPONDER
