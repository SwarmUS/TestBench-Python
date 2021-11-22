from src.parser.AngleCalculatorParameters import AngleCalculatorParameters
import src.parser.utils as utils
import pickle as pkl
import os

class Exporter:
    def __init__(self,exportPath):
        self.dataExportPath = exportPath

    dataExportPath = None
    dataExportPathFolder = None

    def toPickle(self,pairs):
        if not os.path.exists(self.dataExportPath + "/" + "angleParameters"):
            os.makedirs(self.dataExportPath + "/" + "angleParameters")
        self.dataExportPathFolder = self.dataExportPath + "/" + "angleParameters"

        utils.mapDict(self._toPickle, pairs, {k:k for k in pairs.keys()})

    def _toPickle(self,AngleClass: AngleCalculatorParameters,name):
        pkl.dump(AngleClass,open(self.dataExportPathFolder+ "/"+str(name)[-1]+"_angleCalculatorParameters.pkl", 'wb'))

def setPdoaNormalizationFactors(pairs, factors):
    utils.mapDict(_setPdoaNormalizationFactors, pairs, factors)
def _setPdoaNormalizationFactors(AngleClass: AngleCalculatorParameters, factors):
    AngleClass.m_pdoaNormalizationFactors = factors

def setPdoaSlopesCarac(pairs, lineCarac,PDOAscaleFactor):
    utils.mapDict(_setPdoaSlopesCarac, pairs, lineCarac, PDOAscaleFactor)
def _setPdoaSlopesCarac(AngleClass: AngleCalculatorParameters, lineCarac,PDOAscaleFactor):
    AngleClass.m_pdoaSlopes = lineCarac["m"]
    AngleClass.m_pdoaIntercepts = lineCarac["b"]
    AngleClass.m_pdoaNormalizationFactors = PDOAscaleFactor

def setAntennaPairs(pairs):
    pair = {}
    i = 0
    for x in range(0, 3):
        for y in range(0, 3):
            if x != y:
                pair['PDOA'+str(i)] = [x, y]
                i += 1

    utils.mapDict(_setAntennaPairs, pairs, pair)
def _setAntennaPairs(AngleClass: AngleCalculatorParameters, pair):
    AngleClass.m_antennaPairs = pair

def testRead(file):
    return pkl.load(open(file, 'rb'))
