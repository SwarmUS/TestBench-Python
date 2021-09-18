import pandas
from tqdm import tqdm

from src.hiveboard.HiveBoard import HiveBoard
from src.hiveboard.usb_stream import UsbStream

stream = UsbStream('/dev/ttyACM1')
hb = HiveBoard(stream, log=False)

accumulated_data = []

hb.greet()

for ticks in tqdm(range(10)):
    data = hb.read_angle_data()

    for frame in data:
        frame['Encoder Tick'] = ticks
        accumulated_data.append(frame)


dataframe = pandas.DataFrame(accumulated_data)
dataframe.to_csv('output.csv')

hb.kill_receiver()