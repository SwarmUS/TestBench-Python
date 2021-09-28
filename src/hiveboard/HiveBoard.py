from threading import Thread
from time import sleep

from src.hiveboard.proto.message_pb2 import Greeting, Message, InterlocState, UNSUPORTED, STANDBY, ANGLE_CALIB_RECEIVER
from src.hiveboard.proto.proto_stream import ProtoStream


class HiveBoard:
    def __init__(self, proto_stream: ProtoStream, log=True):
        self.uuid = 0
        self.interloc_state = UNSUPORTED

        self.angle_date = []

        self._run = True
        self._proto_stream = proto_stream
        self._rx_thread = Thread(target=self._rx_msg_handler)
        self._rx_thread.start()
        self._log = log

    def kill_receiver(self):
        self._run = False
        self._proto_stream.kill_stream()

    def greet(self):
        greet = Greeting()
        msg = Message()
        msg.greeting.CopyFrom(greet)

        if self._log:
            print("Sending greet to HiveBoard")
        self._proto_stream.write_message_to_stream(msg)
        if self._log:
            print("Waiting for response")
        while self.uuid == 0:
            sleep(0.01)

    def set_interloc_state(self, state):
        msg = Message()
        msg.source_id = self.uuid
        msg.destination_id = self.uuid

        msg.interloc.setState.state = state

        self._proto_stream.write_message_to_stream(msg)

        while self.interloc_state != state:
            sleep(0.01)

    def read_angle_data(self):
        self.angle_date = []

        if self.interloc_state != STANDBY:
            self.set_interloc_state(STANDBY)

        self.set_interloc_state(ANGLE_CALIB_RECEIVER)
        while self.interloc_state != STANDBY:
            sleep(0.01)

        return self.angle_date

    def set_num_angle_frames(self, num_frames):
        msg = Message()
        msg.source_id = self.uuid
        msg.destination_id = self.uuid

        msg.interloc.configure.configureAngleCalibration.numberOfFrames = num_frames
        self._proto_stream.write_message_to_stream(msg)

    def _rx_msg_handler(self):
        while self._run:
            msg = self._proto_stream.read_message_from_stream()

            if msg is None:
                break

            if msg.HasField("greeting"):
                self._handle_greet_response(msg.greeting)
            elif msg.HasField("interloc"):
                self._handle_interloc_message(msg.interloc.output)
            else:
                print(f'Received unhandled message: {msg}')

    def _handle_greet_response(self, greet):
        self.uuid = greet.agent_id
        print(f'Successfully connected to HiveBoard #{self.uuid}')

    def _handle_interloc_message(self, interloc_output):
        if interloc_output.HasField("stateChange"):
            prev_state = InterlocState.Name(interloc_output.stateChange.previousState)
            new_state = InterlocState.Name(interloc_output.stateChange.newState)
            if self._log:
                print(f'Interloc state change {prev_state} --> {new_state}')
            self.interloc_state = interloc_output.stateChange.newState
        else:
            self._handle_angle_data(interloc_output.rawAngleData)

    def _handle_angle_data(self, angle_data):
        for frame in angle_data.frames:
            obj = {
                "Frame ID": frame.frameId
            }

            for beeboard in frame.frameInfos:
                port = beeboard.beeboardPort
                obj[f'BB_{port} Rx Timestamp'] = beeboard.rxTimestamp
                obj[f'BB_{port} SFD Angle'] = beeboard.sfdAngle
                obj[f'BB_{port} Accumulator Angle'] = beeboard.accumulatorAngle
                obj[f'BB_{port} Message ID'] = beeboard.messageId

            self.angle_date.append(obj)

