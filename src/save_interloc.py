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

if not USE_ETHERNET:
    hb_stream = UsbStream('/dev/ttyACM0')
else:
    hb_stream = EthernetStream(55551)
    hb_stream.wait_connection()

hb = HiveBoard(hb_stream, log=True)


class Runner:
    def __init__(self, hiveboard):
        self.running = True
        self.hb = hiveboard

    def signal_handler(self, sig, frame):
        self.running = False

    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler)

        self.hb.greet()
        self.hb.enable_interloc_dumps(True)

        while self.running:
            sleep(1)

        print('Stopping recording')
        self.hb.enable_interloc_dumps(False)
        self.hb.kill_receiver()

        if not os.path.exists('data'):
            os.makedirs('data')

        for remote in hb.interloc_data.keys():
            dataframe = pandas.DataFrame(hb.interloc_data[remote])
            dataframe.to_csv(f'data/{datetime.now().strftime("%Y%m%d_%H%M%S")}-hb_{remote}.csv')


runner = Runner(hb)
runner.run()


