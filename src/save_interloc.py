import signal

import pandas
import os
from time import sleep
from datetime import datetime

from src.hiveboard.HiveBoard import HiveBoard
from src.hiveboard.proto.ethernet_stream import EthernetStream
from src.hiveboard.usb_stream import UsbStream

# To use ethernet, you must have a static IP of 192.168.1.101 on submask 255.255.255.0
USE_ETHERNET = False
distance = '_0p22_5m' # distance btw BB and distance between HB

if not USE_ETHERNET:
    hb_stream = UsbStream('/dev/ttyACM2')
else:
    hb_stream = EthernetStream(55551)
    hb_stream.wait_connection()

hb = HiveBoard(hb_stream, log=True)

accumulated_data = []
run = True


def signal_handler(sig, frame):
    run = False


signal.signal(signal.SIGINT, signal_handler)

hb.greet()
hb.enable_interloc_dumps(True)

while run:
    sleep(1)

print('Stopping recording')
hb.enable_interloc_dumps(False)
hb.kill_receiver()

if not os.path.exists('data'):
    os.makedirs('data')

for remote in hb.interloc_data.keys():
    dataframe = pandas.DataFrame(hb.interloc_data[remote])
    dataframe.to_csv('data/' + datetime.now().strftime("%Y%m%d_%H%M%S") + '-hb_' + remote +'.csv')
