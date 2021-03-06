from threading import Thread
from time import sleep

from src.hiveboard.proto.message_pb2 import Greeting, Message, InterlocState, UNSUPORTED, STANDBY, ANGLE_CALIB_RECEIVER
from src.hiveboard.proto.message_pb2 import GetNeighborsListRequest, HiveMindHostApiRequest, Request, GetNeighborRequest
from src.hiveboard.proto.message_pb2 import GetNeighborsListResponse, HiveMindHostApiResponse, Response, GetNeighborResponse
from src.hiveboard.proto.proto_stream import ProtoStream
from src.AngleCalculatorParameters import AngleCalculatorParameters


def _fill_proto_list(proto_field, values_list):
    for i, val in enumerate(values_list):
        proto_field[i] = val


class HiveBoard:
    def __init__(self, proto_stream: ProtoStream, log=True):
        self.uuid = 0
        self.interloc_state = UNSUPORTED

        self.angle_date = []
        self.interloc_data = {}

        self._run = True
        self._proto_stream = proto_stream
        self._rx_thread = Thread(target=self._rx_msg_handler)
        self._rx_thread.start()
        self._log = log

        self.neighbors_list_callback = None
        self.neighbor_position_callback = None

        self._id_map = {
            0: 0,
            1: 1,
            5: 2
        }
        # self._decision_matrix = [[0, 0, 1], [1, 0, 1], [0, 0, 0]]
        self._decision_matrix = [[-1, 0, 1], [1, -1, 1], [0, 0, -1]]

    def set_neighbor_list_callback(self, callback):
        self.neighbors_list_callback = callback

    def set_neighbor_position_callback(self, callback):
        self.neighbor_position_callback = callback

    def set_neighbor_list_callback(self, callback):
        self.neighbors_list_callback = callback

    def set_neighbor_position_callback(self, callback):
        self.neighbor_position_callback = callback

    def kill_receiver(self):
        self._run = False
        self._proto_stream.kill_stream()

    def greet(self):
        greet = Greeting()
        # Patch for message to be longer than 4 bytes so that python can deserialize its own messages
        greet.agent_id = 1
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

    def enable_interloc_dumps(self, enabled: bool):
        msg = Message()
        msg.source_id = self.uuid
        msg.destination_id = self.uuid

        msg.interloc.configure.configureInterlocDumps.enable = enabled
        self._proto_stream.write_message_to_stream(msg)

    def set_angle_parameters(self, params: AngleCalculatorParameters, orientation_offset: float):
        msg = Message()
        msg.source_id = self.uuid
        msg.destination_id = self.uuid

        pair_id = self._id_map[params.m_pairID]

        msg.interloc.configure.configureAngleParameters.anglePairId = pair_id

        msg.interloc.configure.configureAngleParameters.antennas.extend(params.m_antennaPairs)
        msg.interloc.configure.configureAngleParameters.slopeDecision.extend(self._decision_matrix[pair_id])

        msg.interloc.configure.configureAngleParameters.pdoaNormalizationFactor = params.m_pdoaNormalizationFactors
        msg.interloc.configure.configureAngleParameters.pdoaSlopes.extend(params.m_pdoaSlopes)
        msg.interloc.configure.configureAngleParameters.pdoaIntercepts.extend(params.m_pdoaIntercepts)

        msg.interloc.configure.configureAngleParameters.boardOrientationOffset = orientation_offset

        self._proto_stream.write_message_to_stream(msg)

    def send_get_neighbors_request(self, destination: int):
        neighbors_request = GetNeighborsListRequest()

        hivemind_api_request = HiveMindHostApiRequest()
        hivemind_api_request.neighbors_list.CopyFrom(neighbors_request)

        request = Request()
        request.hivemind_host.CopyFrom(hivemind_api_request)

        msg = Message()
        msg.source_id = self.uuid
        msg.destination_id = destination
        msg.request.CopyFrom(request)

        self._proto_stream.write_message_to_stream(msg)

    def send_get_neighbor_position_request(self, destination: int, neighbor_id: id):
        neighbor_position_request = GetNeighborRequest()
        neighbor_position_request.neighbor_id = neighbor_id

        hivemind_host_api_request = HiveMindHostApiRequest()
        hivemind_host_api_request.neighbor.CopyFrom(neighbor_position_request)

        request = Request()
        request.hivemind_host.CopyFrom(hivemind_host_api_request)

        msg = Message()
        msg.source_id = self.uuid
        msg.destination_id = destination
        msg.request.CopyFrom(request)

        self._proto_stream.write_message_to_stream(msg)

    def send_get_neighbors_request(self, destination: int):
        neighbors_request = GetNeighborsListRequest()

        hivemind_api_request = HiveMindHostApiRequest()
        hivemind_api_request.neighbors_list.CopyFrom(neighbors_request)

        request = Request()
        request.hivemind_host.CopyFrom(hivemind_api_request)

        msg = Message()
        msg.source_id = self.uuid
        msg.destination_id = destination
        msg.request.CopyFrom(request)

        self._proto_stream.write_message_to_stream(msg)

    def send_get_neighbor_position_request(self, destination: int, neighbor_id: id):
        neighbor_position_request = GetNeighborRequest()
        neighbor_position_request.neighbor_id = neighbor_id

        hivemind_host_api_request = HiveMindHostApiRequest()
        hivemind_host_api_request.neighbor.CopyFrom(neighbor_position_request)

        request = Request()
        request.hivemind_host.CopyFrom(hivemind_host_api_request)

        msg = Message()
        msg.source_id = self.uuid
        msg.destination_id = destination
        msg.request.CopyFrom(request)

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
            elif msg.HasField("response"):
                self._parse_and_handle_response(msg.response)
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
        elif interloc_output.HasField("rawAngleData"):
            self._handle_angle_data(interloc_output.rawAngleData)
        elif interloc_output.HasField("interlocDump"):
            self._handle_interloc_dump(interloc_output.interlocDump)

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

    def _handle_interloc_dump(self, dump):
        print("Received interloc updates")

        for update in dump.positionUpdates:
            id = update.neighbor_id

            obj = {
                "Distance": update.position.distance,
                "Azimuth": update.position.azimuth,
                "LoS": update.position.in_los
            }

            if id in self.interloc_data.keys():
                self.interloc_data[id].append(obj)
            else:
                self.interloc_data[id] = [obj]

    def _parse_and_handle_response(self, response : Response):
        if response.HasField("hivemind_host"):
            hivemind_host_api_response = response.hivemind_host
            if hivemind_host_api_response.HasField("neighbors_list") and self.neighbors_list_callback:
                neighbors_list = hivemind_host_api_response.neighbors_list
                self.neighbors_list_callback(neighbors_list.neighbors)
            elif hivemind_host_api_response.HasField("neighbor") and self.neighbor_position_callback:
                neighbor = hivemind_host_api_response.neighbor
                self.neighbor_position_callback(neighbor)





