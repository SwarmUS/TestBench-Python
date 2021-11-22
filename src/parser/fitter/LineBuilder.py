# from https://matplotlib.org/stable/users/event_handling.html
from matplotlib import collections  as mc

class LineBuilder:
    def __init__(self, line,ax):
        self.line = [line]
        self.ax = ax
        self.eventCounter = 0
        self.nbLine = 0
        self.xs = []
        self.ys = []
        self.cid = self.line[-1].figure.canvas.mpl_connect('button_press_event', self)
        self.ms = []
        self.bs = []


    def __call__(self, event):
        if event.inaxes!=self.line[-1].axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.eventCounter += 1
        self.line[-1].set_data(self.xs, self.ys)
        if self.eventCounter > 1:
            return self.addLine()

    def addLine(self):
        self.eventCounter = 0
        m = (self.ys[1 + 2 * self.nbLine] - self.ys[0 + 2 * self.nbLine]) / (
                self.xs[1 + 2 * self.nbLine] - self.xs[0 + 2 * self.nbLine])
        b = self.ys[1 + 2 * self.nbLine] - m * self.xs[1 + 2 * self.nbLine]
        self.ms.append(m)
        self.bs.append(b)
        self.line[-1].figure.canvas.draw()
        lineNew, = self.ax.plot([0], [0],'r')
        self.line.append(lineNew)
        self.cid = self.line[-1].figure.canvas.mpl_connect('button_press_event', self)
        self.xs=[]
        self.ys=[]