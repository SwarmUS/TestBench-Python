# from https://matplotlib.org/stable/users/event_handling.html
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

class PointExtracter:
    def __init__(self,ax):
        self.scat = None
        self.ax = ax
        self.nbLine = 0
        self.xs = []
        self.ys = []
        self.cid = self.ax.figure.canvas.mpl_connect('button_press_event', self)
        self.ms = []
        self.ptCnt = 0


    def __call__(self, event):
        if self.ptCnt < 1:
            self.scat = self.ax.scatter([event.xdata],[event.ydata],c='r',zorder=10)
            self.ys.append(event.ydata)
            self.scat.axes.figure.canvas.draw_idle()
        else:
            self.addPoint([event.xdata,event.ydata])
            self.ys.append(event.ydata)
            # return [round(x) for x in self.xs]

    def addPoint(self,new_point, c='r'):
        old_off = self.scat.get_offsets()
        new_off = np.concatenate([old_off, np.array(new_point, ndmin=2)])
        old_c = self.scat.get_facecolors()
        new_c = np.concatenate([old_c, np.array(matplotlib.colors.to_rgba(c), ndmin=2)])

        self.scat.set_offsets(new_off)
        self.scat.set_facecolors(new_c)

        self.scat.axes.figure.canvas.draw_idle()