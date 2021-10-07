import pandas
import os
from time import sleep
from tqdm import tqdm

from datetime import datetime

from hiveboard.HiveBoard import HiveBoard
from hiveboard.proto.ethernet_stream import EthernetStream
from hiveboard.usb_stream import UsbStream
from turning_station.TurningStation import TurningStation, tickToAngle

# To use ethernet, you must have a static IP of 192.168.1.101 on submask 255.255.255.0
USE_ETHERNET = True

if not USE_ETHERNET:
    hb_stream = UsbStream('/dev/ttyACM0')
else:
    hb_stream = EthernetStream(55551)
    hb_stream.wait_connection()

# testbench = TurningStation('/dev/ttyACM1', 115200)

hb = HiveBoard(hb_stream, log=False)

accumulated_data = []

hb.greet()
while True:
    sleep(1)

hb.set_num_angle_frames(100)

# TODO: Add way to turn until position is 0
sleep(2) # arduino needs to reboot after uart initialisation
#testbench.resetPosition()

if not os.path.exists('data'):
    os.makedirs('data')

for ticks in tqdm(range(10, 100, 10)):
    #testbench.goToTick(ticks)
    data = hb.read_angle_data()

    for frame in data:
        frame['Encoder Tick'] = ticks
        frame['Angle'] = tickToAngle(ticks)
        accumulated_data.append(frame)

    sleep(0.5)


dataframe = pandas.DataFrame(accumulated_data)
dataframe.to_csv('data/' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.csv')

hb.kill_receiver()
