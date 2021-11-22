from pylab import *
import numpy as np
from src.parser.fitter.LineBuilder import LineBuilder
from src.parser.fitter.PointExtracter import PointExtracter


def plotPDOA(dPDOA, mdPDOA, sdPDOA,namePDOA='PDOA0',dataPath=None,createFig=False,reciproque=False):
    if createFig is not False:
        fig = plt.figure()

    if type(namePDOA) is list:
        for name in namePDOA:
            l = list(mdPDOA[name].items())
            k = list(sdPDOA[name].items())
            x, y = zip(*l)
            _, yerr = zip(*k)
            if reciproque:
                plt.errorbar(y, x, xerr=yerr, fmt='.', label='moy ' + name)
                plt.ylabel("Angle reel (deg)")
                plt.xlabel("Angle mesuré (" + "PDOA" + ") (deg)")
            else:
                plt.errorbar(x, y, yerr, fmt='.', label='moy ' + name)
                plt.xlabel("Angle reel (deg)")
                plt.ylabel("Angle mesuré (" + "PDOA" + ") (deg)")
        plt.title("Angle mesuré (" + 'PDOA' + ") en fonction de l'angle réel")
    else:

        l = list(mdPDOA[namePDOA].items())
        k = list(sdPDOA[namePDOA].items())
        x, y = zip(*l)
        _, yerr = zip(*k)
        if reciproque:

            # plot all data
            plotAllData(dPDOA,namePDOA)

            l = list(mdPDOA[namePDOA].items())
            k = list(sdPDOA[namePDOA].items())
            x, y = zip(*l)
            _, yerr = zip(*k)
            plt.errorbar(y, x, xerr=yerr, fmt='.', label='moy ' + namePDOA)
            plt.ylabel("Angle reel (deg)")
            plt.xlabel("Angle mesuré (" + "PDOA" + ") (deg)")
        else:
            # plot all data
            plotAllData(dPDOA,namePDOA)
            # plt.errorbar(x, y, yerr, fmt='.', label='moy ' + namePDOA)
            plt.plot(x, y,".", label='moy ' + namePDOA)
            plt.xlabel("Angle reel (deg)")
            plt.ylabel("Angle mesuré (" + namePDOA + ") (deg)")
        plt.title("Angle mesuré (" + namePDOA + ") en fonction de l'angle réel")
    plt.legend()

    if type(namePDOA) is list:
        if dataPath != None:
            plt.savefig(dataPath + '/' + '_'.join(map(str, namePDOA)) + '.png')
    else:
        if dataPath != None:
            plt.savefig(dataPath + '/' + namePDOA + '.png')

    if createFig:
        return fig

def plotAllData(dic,name):
    allData = []
    for key in dic[name]:
        allData.extend(list(map(lambda e: (key, e), dic[name][key])))
    xall, yall = zip(*allData)
    plt.plot(xall, yall, '.')

def extractSlopes(dPDOA, mdPDOA, namePDOA = "PDOA0"):
    fig, ax = plt.subplots()
    gca().set_position((.1, .2, .8, .73))

    plotAllData(dPDOA,namePDOA)

    # plot mean data
    l = list(mdPDOA[namePDOA].items())
    x, y = zip(*l)
    plt.plot(x, y, '.',color="orange", label = "Mean values")

    line, = ax.plot([0], [0],'r')  # empty line
    # manual line fitter
    lineBuilder = LineBuilder(line,ax)

    plt.legend()
    plt.ylabel("Measured angle (deg)")
    plt.xlabel("Real angle (deg)")
    plt.title(f"Draw 2-3 segments to represent {namePDOA}")
    t = "Click on the starting and ending point of each line.\nThe slope values will be saved on exit"
    figtext(.02, .02, t)
    plt.show()

    ms , bs = sortSlopes(lineBuilder.ms,lineBuilder.bs)

    slopes = {}
    slopes[namePDOA] = {}
    slopes[namePDOA]["m"] = ms
    slopes[namePDOA]["b"] = bs

    return slopes


def sortSlopes(ms,bs):
    goodMs = ms.copy()
    goodBs = bs.copy()

    if len(ms) != len(bs):
        raise Exception("Slope Selection Error")
    elif len(ms) > 3 or len(ms) < 2:
        raise Exception("Slope Number Error")
    elif len(ms) == 2:
        return sorted(goodMs), sorted(goodBs,reverse=True)
    else: #len(ms) == 3
        return sorted(goodMs[0:-1]), sorted(goodBs[0:-1],reverse=True)



def plotSTDEV(sdPDOA,sdTDOA=None,nameTDOA = 'TDOA0',namePDOA = 'PDOA0',dataPath=None):
    fig = plt.figure()
    if type(namePDOA) is list:
        for i,nameP in enumerate(namePDOA):
            nameT = nameTDOA[i]
            if sdTDOA is not None:
                l = list(sdTDOA[nameT].items())
                x, y = zip(*l)
                plt.plot(x, y, '.', label='stdev ' + nameT)

            k = list(sdPDOA[nameP].items())
            x, y = zip(*k)
            plt.plot(x, y, '.', label='stdev ' + nameP)
    else:
        if sdTDOA is not None:
            l = list(sdTDOA[nameTDOA].items())
            x, y = zip(*l)
            plt.plot(x,y,'.r',label='stdev '+nameTDOA)

        k = list(sdPDOA[namePDOA].items())
        x, y = zip(*k)
        plt.plot(x,y,'.',label='stdev '+namePDOA)
    plt.title("Écart type de 100 val en fonction de l'angle réel")
    plt.xlabel("Angle reel (deg)")
    plt.ylabel("Écart type (deg)")
    plt.legend()

    if dataPath != None:
        if type(nameTDOA) is list:
            if dataPath != None:
                plt.savefig(dataPath + '/stdDev_' + '_'.join(map(str, nameTDOA)) + '.png')
            else:
                plt.savefig(dataPath+'/stdDev_'+nameTDOA+'_'+namePDOA+'.png')

    return fig

def plotPDOAReverse(pdoaReverse,mdPDOA):
    plot([list(mdPDOA.keys())[x] for x in pdoaReverse],[mdPDOA[list(mdPDOA.keys())[x]] for x in pdoaReverse],"xk")

def extractSlopeExtremums(dPDOA, mdPDOA, namePDOA = "PDOA0"):
    fig, ax = plt.subplots()
    gca().set_position((.1, .2, .8, .73))

    # plot all data
    plotAllData(dPDOA,namePDOA)

    # plot mean data
    l = list(mdPDOA[namePDOA].items())
    x, y = zip(*l)
    plt.plot(x, y, '.', color="orange", label="Mean values")

    # manual point finder    .
    pointExtracter = PointExtracter(ax)

    plt.legend()
    plt.ylabel("Measured angle (deg)")
    plt.xlabel("Real angle (deg)")
    plt.title(f"Select points to represent {namePDOA} desired offset")
    t = "Many points can be selected, the mean of the *y axis* will be used as the offset.\n" \
        "If the sin is not wrapping, no points need to be selected, as no offset needs to be applied "
    figtext(.02, .02, t)

    plt.show()
    if len(pointExtracter.ys) > 1:
        meanVal = np.mean(pointExtracter.ys)
        return -meanVal
    else:
        return 0
