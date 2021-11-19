from scipy import signal
import numpy as np
import src.parser.utils as utils


def diff(d):
    return utils.mapDict(_diff, d)

def findMin(d):
    return utils.mapDict(_findMin, d)

def filterLP(d):
    return utils.mapDict(_filterLP, d)

def offset(mdPDOA):
    return utils.mapDict(_offset, mdPDOA)


def _diff(dic):
    prevVal = 0
    out = []
    for angle in dic.keys():
        out.append(abs(prevVal - dic[angle]))
        prevVal = dic[angle]
    # plt.plot(out)
    # plt.show()

    return out

def _findMin(lis):
     mins = signal.argrelextrema(lis, np.less,order=30)
     out = [val for val in mins[0]]


     if len(out) > 2:
        out = np.delete(out, np.argmax(lis[out]))

     if len (out) < 2:
         if np.argmin(lis) < out:
             out = np.append(np.argmin(lis),out)
         else:
             out = np.append(out, int(np.argmin(lis)-1))
     return list(out)

def _filterLP(lis):
    b, a = signal.butter(1, 0.5)
    sig = signal.filtfilt(b, a, lis)
    # plt.plot(sig)
    # plt.title("Dérivée du PDOA suivi d'un low pass")
    # plt.xlabel("index")
    # plt.ylabel("Signal dérivé")
    # plt.show()
    return sig

def _offset(mdPDOA):
    meanVal = np.mean(list(mdPDOA.values()))
    return meanVal