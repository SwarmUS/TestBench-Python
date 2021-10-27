import pickle as pkl
from src.hiveboard.HiveBoard import HiveBoard
from src.hiveboard.proto.ethernet_stream import EthernetStream
from src.hiveboard.usb_stream import UsbStream

# To use ethernet, you must have a static IP of 192.168.1.101 on submask 255.255.255.0
USE_ETHERNET = False
PARAMETERS_FILE = 'parameters/5_angleCalculatorParameters.pkl'

if not USE_ETHERNET:
    hb_stream = UsbStream('/dev/ttyACM0')
else:
    hb_stream = EthernetStream(55551)
    hb_stream.wait_connection()

hb = HiveBoard(hb_stream, log=True)

hb.greet()

for i in [0, 1, 5]:
    params = pkl.load(open(f'parameters/{i}_angleCalculatorParameters.pkl', 'rb'))
    hb.set_angle_parameters(params)

hb.kill_receiver()

