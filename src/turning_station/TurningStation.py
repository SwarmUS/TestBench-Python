import serial
from time import sleep

class TurningStation():
    def __init__(self,port,baudrate=112500):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate
        )
        sleep(2) # wait for reboot time

    def __del__(self):
        self.ser.close()

    def sendMsg(self,msg):
        self.ser.write(msg.encode())
        sleep(0.2) #watit for processing time on arduino

    def setAngle(self,angle):
        msg = "turn:"+str(angle)
        print(msg)
        self.sendMsg(msg)

    def setEnable(self,enable):
        msg = "enable:"+str(enable)
        print(msg)
        self.sendMsg(msg)

    def resetPosition(self):
        msg = "position_reset"
        print(msg)
        self.sendMsg(msg)

    def setDirection(self,direction):
        msg = "direction:"+str(direction)
        print(msg)
        self.sendMsg(msg)

    def getStatus(self):
        sleep(1)
        self.sendMsg("status")
        return  self.ser.read_all()