import signal

import pandas
import os
import time
from datetime import datetime

from src.hiveboard.HiveBoard import HiveBoard
from src.hiveboard.proto.ethernet_stream import EthernetStream
from src.hiveboard.usb_stream import UsbStream

# To use ethernet, you must have a static IP of 192.168.1.101 on submask 255.255.255.0
USE_ETHERNET = False

if not USE_ETHERNET:
    hb_stream = UsbStream('/dev/ttyACM0')
else:
    hb_stream = EthernetStream(7001)
    hb_stream.wait_connection()

hb = HiveBoard(hb_stream, log=True)


class Runner:
    def __init__(self, hiveboard):
        self.running = True
        self.hb = hiveboard
        self.time_start = 0

    def signal_handler(self, sig, frame):
        self.running = False
        
    def function_request_handler(self, function_call_request):
        if function_call_request.function_name == "timeStart":
            self.hb.send_function_call(hb.uuid, "timeLoopBuzz", [self.hb.uuid], True)
            print("start time")
            self.time_start = time.time_ns()
        elif function_call_request.function_name == "timeEnd":
            ellapsed = time.time_ns() - self.time_start
            print(f"Elapsed time {ellapsed/1e6}")


    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.hb.set_function_request_call_callback(self.function_request_handler)

        self.hb.greet()

        while self.running:
            time.sleep(1)

        print('Stopping')
        self.hb.kill_receiver()


runner = Runner(hb)
runner.run()


