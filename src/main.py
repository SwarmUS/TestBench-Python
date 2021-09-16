from src.hiveboard.proto.message_pb2 import Greeting, Message
from src.hiveboard.usb_stream import UsbStream

HIVEMIND_ID = 0
REMOTE_ID = 42

x = UsbStream('/dev/ttyACM1')

greet = Greeting()
greet.agent_id = HIVEMIND_ID

greet_msg = Message()
greet_msg.source_id = 0
greet_msg.destination_id = 0xff
greet_msg.greeting.CopyFrom(greet)

print("Attempting to greet with HiveMind")
x.write_message_to_stream(greet_msg)
receivedMessage = x.read_message_from_stream()

print(receivedMessage)