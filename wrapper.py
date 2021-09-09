from wrapping.TurningStation import TurningStation
from time import sleep
import csv
from datetime import datetime
import os


header = ['Encoder tick', 'angle', 'TDOA 1', 'TDOA 2', 'TDOA 3']

def main():
    if not os.path.exists('data'):
        os.makedirs('data')

    f = open('data/'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.csv', 'w',newline='')
    writer = csv.writer(f)
    writer.writerow(header)

    testBench = TurningStation('COM15',115200)
    #init HB
    for angle in [100, 0, 150, 0, 250, 350]:

        testBench.resetPosition()
        testBench.setAngle(angle)
        testBench.setEnable(1)

        while testBench.getStatus().decode() != "done":
                sleep(0.3)

        # get TDOA measurements from HB

        writer.writerow([angle,angle/2048*360,0,0,0])

    f.close()


if __name__ == "__main__":
    main()
