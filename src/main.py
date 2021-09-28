import pandas
import os
from time import sleep
from tqdm import tqdm

from datetime import datetime

from src.hiveboard.HiveBoard import HiveBoard
from src.hiveboard.usb_stream import UsbStream
from src.turning_station.TurningStation import TurningStation, tickToAngle

hb_stream = UsbStream('/dev/ttyACM0')
testbench = TurningStation('/dev/ttyACM1', 115200)

hb = HiveBoard(hb_stream, log=False)

accumulated_data = []

hb.greet()
hb.set_num_angle_frames(25)

# TODO: Add way to turn until position is 0
sleep(2) # arduino needs to reboot after uart initialisation
testbench.resetPosition()

if not os.path.exists('data'):
    os.makedirs('data')

for ticks in tqdm(range(10, 500, 10)):
    testbench.goToTick(ticks)
    data = hb.read_angle_data()

    for frame in data:
        frame['Encoder Tick'] = ticks
        frame['Angle'] = tickToAngle(ticks)
        accumulated_data.append(frame)

    sleep(0.5)


dataframe = pandas.DataFrame(accumulated_data)
dataframe.to_csv('data/' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.csv')

hb.kill_receiver()
