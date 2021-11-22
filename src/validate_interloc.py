import pickle as pkl
from datetime import datetime
from time import sleep, strftime

import pandas
from tqdm import tqdm

from src.hiveboard.HiveBoard import HiveBoard
from src.hiveboard.proto.ethernet_stream import EthernetStream
from src.hiveboard.proto.message_pb2 import STANDBY, OPERATING
from src.hiveboard.usb_stream import UsbStream

# To use ethernet, you must have a static IP of 192.168.1.101 on submask 255.255.255.0
from src.turning_station.TurningStation import tickToAngle, TurningStation

USE_ETHERNET = False

REMOTE_HB_ID = 1
NUM_DATA_POINTS_PER_ANGLE = 20

if not USE_ETHERNET:
    hb_stream = UsbStream('/dev/ttyACM0')
else:
    hb_stream = EthernetStream(55551)
    hb_stream.wait_connection()

hb = HiveBoard(hb_stream, log=True)
testbench = TurningStation('/dev/ttyACM1', 115200)

data = []

hb.greet()
hb.set_interloc_state(STANDBY)

# TODO: Add way to turn until position is 0
sleep(2) # arduino needs to reboot after uart initialisation
testbench.resetPosition()

stepSize = 20
destination = 2060
for ticks in tqdm(range(0, destination, stepSize)):
    hb.enable_interloc_dumps(True)
    hb.set_interloc_state(OPERATING)

    while len(hb.interloc_data.keys()) == 0 or REMOTE_HB_ID not in hb.interloc_data.keys() or len(
            hb.interloc_data[REMOTE_HB_ID]) < NUM_DATA_POINTS_PER_ANGLE:
        sleep(1)

    hb.enable_interloc_dumps(False)
    hb.set_interloc_state(STANDBY)

    testbench.goToTick(stepSize)

    for data_point in hb.interloc_data[REMOTE_HB_ID]:
        data_point_copy = data_point.copy()
        data_point_copy['ticks'] = ticks
        data_point_copy['angle'] = tickToAngle(ticks)

        data.append(data_point_copy)

    hb.interloc_data[REMOTE_HB_ID] = []

    sleep(0.5)
    testbench.resetPosition()

dataframe = pandas.DataFrame(data)
dataframe.to_csv(f'data/validation_{datetime.now()}.{strftime("%Y%m%d_%H%M%S")}.csv')

sleep(1)
hb.enable_interloc_dumps(False)
hb.set_interloc_state(OPERATING)
hb.kill_receiver()
