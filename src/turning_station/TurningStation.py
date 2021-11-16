import serial
from time import sleep

class TurningStation():
    def __init__(self,port,baudrate=112500):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=0.5
        )
        sleep(2) # wait for reboot time

    def __del__(self):
        self.ser.close()

    def sendMsg(self,msg):
        # print(msg)
        self.ser.write(msg.encode('utf-8'))
        sleep(0.5) #wait for processing time on arduino

        response = self.ser.read_until().decode()
        if response != "ack\n": # retry on error
            self.ser.flush()
            sleep(0.5)
            self.sendMsg(msg)

    def setAngle(self,angle):
        msg = "turn:"+str(angle)+";"
        self.sendMsg(msg)

    def setEnable(self,enable):
        msg = "enable:"+str(enable) + ";"
        self.sendMsg(msg)

    def resetPosition(self):
        msg = "position_reset;"
        self.sendMsg(msg)

    def setDirection(self,direction):
        msg = "direction:"+str(direction) + ";"
        self.sendMsg(msg)

    def getStatus(self):
        # sleep(0.1)
        self.sendMsg("status;")
        return self.ser.read_all()

    def getPosition(self):
        # sleep(1)
        self.sendMsg("positionis;")
        pos =  self.ser.read_until().decode()

        while not pos[0:-1].isnumeric():
            self.ser.flush()
            self.sendMsg("positionis;")
            pos = self.ser.read_until().decode()

        # print(int(pos))
        return pos

    def goToTick(self, tick):
        self.setAngle(tick)
        self.setEnable(1)

        while self.getStatus().decode() != "done\n":
                sleep(0.1)

        position = self.getPosition()

        if int(position) > (tick + 5):
            self.goToTick(tick)
        elif int(position) < (tick - 5):
            self.goToTick(tick)








def tickToAngle(tick):
    return tick/2048*360
