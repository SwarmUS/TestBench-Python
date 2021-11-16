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
distance = "0p024_2mOfficial"
if not USE_ETHERNET:
    hb_stream = UsbStream('COM16')
else:
    hb_stream = EthernetStream(7001)
    hb_stream.wait_connection()

testbench = TurningStation('COM15', 115200)

hb = HiveBoard(hb_stream, log=False)

accumulated_data = []

hb.greet()


# TODO: Add way to turn until position is 0
sleep(2) # arduino needs to reboot after uart initialisation
testbench.resetPosition()

if not os.path.exists('data'):
    os.makedirs('data')

stepSize = 20
num_frames = 100
for ticks in tqdm(range(0, 2060, stepSize)):
    hb.set_num_angle_frames(num_frames)
    data = hb.read_angle_data()

    # Ensure we receive all requested data as HB could return less
    while len(data) < num_frames:
        hb.set_num_angle_frames(num_frames - len(data))
        data += hb.read_angle_data()

    testbench.goToTick(stepSize)
    posTick = int(testbench.getPosition())
    for frame in data:
        frame['Encoder Tick'] = ticks
        frame['Angle'] = tickToAngle(ticks)
        accumulated_data.append(frame)
    sleep(0.5)
    testbench.resetPosition()

dataframe = pandas.DataFrame(accumulated_data)
dataframe.to_csv('data/' + datetime.now().strftime("%Y%m%d_%H%M%S") +distance+ '.csv')

hb.kill_receiver()
hb_stream.kill_stream()
