import pandas
from tqdm import tqdm

from src.hiveboard.HiveBoard import HiveBoard
from src.hiveboard.usb_stream import UsbStream
from src.turning_station.TurningStation import TurningStation, tickToAngle

hb_stream = UsbStream('/dev/ttyACM1')
#testbench = TurningStation('COM15', 115200)

hb = HiveBoard(hb_stream, log=False)

accumulated_data = []

hb.greet()
hb.set_num_angle_frames(25)

# TODO: Add way to turn until position is 0
#testbench.resetPosition()

for ticks in tqdm(range(0, 2048, 10)):
    #testbench.goToTick(ticks)
    data = hb.read_angle_data()

    for frame in data:
        frame['Encoder Tick'] = ticks
        frame['Angle'] = tickToAngle(ticks)
        accumulated_data.append(frame)


dataframe = pandas.DataFrame(accumulated_data)
dataframe.to_csv('output.csv')

hb.kill_receiver()