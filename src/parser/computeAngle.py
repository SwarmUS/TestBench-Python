import numpy as np
import src.parser.utils as utils

def minMaxAverage(TDOA,phaseReverse):
    return utils.mapDict(_minMaxAverage, TDOA, phaseReverse)

def _minMaxAverage(TDOA,phaseReverse):
    mean = []
    for i in [0, 1]:
        min = int(phaseReverse[i]-5) if (phaseReverse[i]-5) > 0 else 0
        max = int(phaseReverse[i]+5) if (phaseReverse[i]+5) < len(TDOA.values()) else int(len(TDOA.values())-1)

        mean.append(np.mean(list({list(TDOA)[val]: np.mean(TDOA[list(TDOA)[val]]) for val in
                            range(min, max)}.values())))

    return mean

def PDOA(d,columnsSFD,columnsCIR,angles,offset=None):
    columnsSFD = columnsSFD[0]
    columnsCIR = columnsCIR[0]
    numItr = 2**len(columnsSFD) - 2**(len(columnsSFD)-2)
    name = []
    for itr in range(numItr):
        name.append('PDOA'+str(itr))


    PDOA = {}
    i = 0
    for col1,_ in enumerate(columnsSFD):
        for col2,_ in enumerate(columnsSFD):
            if col1 != col2:
                PDOA[name[i]] = {}
                for a in angles:
                    sfd1 =  np.array(d[a][columnsSFD[col1]])
                    sfd2 =  np.array(d[a][columnsSFD[col2]])
                    fp1 =  np.array(d[a][columnsCIR[col1]])
                    fp2 =  np.array(d[a][columnsCIR[col2]])

                    part1 = np.add(np.subtract(np.subtract(fp1,sfd1),fp2),sfd2)-np.pi/2
                    part2 = np.mod(part1,2*np.pi)
                    if offset is None:
                        PDOA[name[i]][a] = part2
                    else:
                        scaleFactor = 1
                        theta = np.mod((part2 + offset[name[i]]), 2 * np.pi) - np.pi
                        PDOA[name[i]][a] = np.arcsin(theta/np.pi) * 180/np.pi * scaleFactor
                i = i+1
    return PDOA

def stats(d):
    mean = {x: {a: np.mean(d[x][a]) for a in d[x].keys()} for x in d.keys()}
    stdev = {x: {a: np.std(d[x][a]) for a in d[x].keys()} for x in d.keys()}
    return mean,stdev

def _filterSTD(sdPDOA):
    rem = []
    for d in sdPDOA:
        if sdPDOA[d] > 15:
            rem.append(d)
    return rem

def filterSTD(sdPDOA):
    return utils.mapDict(_filterSTD, sdPDOA)

def removeAnormalStdDev(mdPDOA,sdPDOA, mdTDOA, sdTDOA=None):
     valOut = filterSTD(sdPDOA)

     for i,name in enumerate(valOut):
         for rem in valOut[name]:
             mdPDOA[name].pop(rem)
             sdPDOA[name].pop(rem)
             mdTDOA[list(mdTDOA)[i]].pop(rem)
             if sdTDOA is not None:
                 sdTDOA[list(mdTDOA)[i]].pop(rem)
     return mdPDOA,sdPDOA,mdTDOA,sdTDOA

def mean(dic):
    return utils.mapDict(_mean, dic)
def _mean(val):
    return np.mean(list(val.values()))