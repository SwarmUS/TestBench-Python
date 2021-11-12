import pandas
import os
from time import sleep
from tqdm import tqdm

from datetime import datetime

from src.hiveboard.HiveBoard import HiveBoard
from src.hiveboard.proto.ethernet_stream import EthernetStream
from src.hiveboard.usb_stream import UsbStream
from src.turning_station.TurningStation import TurningStation, tickToAngle


# To use ethernet, you must have a static IP of 192.168.1.101 on submask 255.255.255.0
USE_ETHERNET = True
distance = "0p024_2m"
if not USE_ETHERNET:
    hb_stream = UsbStream('COM16')
else:
    hb_stream = EthernetStream(55551)
    hb_stream.wait_connection()

testbench = TurningStation('COM15', 115200)

hb = HiveBoard(hb_stream, log=False)

accumulated_data = []

hb.greet()
hb.set_num_angle_frames(100)

# TODO: Add way to turn until position is 0
sleep(2) # arduino needs to reboot after uart initialisation
testbench.resetPosition()

if not os.path.exists('data'):
    os.makedirs('data')
step = 20
destination = 2060
for ticks in tqdm(range(0, destination, step)):
    data = hb.read_angle_data()
    pos = int(testbench.getPosition())
    for frame in data:
        frame['Encoder Tick'] = pos
        frame['Angle'] = tickToAngle(ticks)
        accumulated_data.append(frame)

    testbench.goToTick(step)

    sleep(0.2)
    testbench.resetPosition()

dataframe = pandas.DataFrame(accumulated_data)
dataframe.to_csv('data/' + datetime.now().strftime("%Y%m%d_%H%M%S") +distance+ '.csv')

hb.kill_receiver()
hb_stream.kill_stream()
