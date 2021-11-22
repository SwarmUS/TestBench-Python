import matplotlib.pyplot as plt
import pandas as pd
import src.parser.parsing as parse
import src.parser.computeAngle as compute
import src.parser.plotter as p
import os
import src.parser.export as export
import src.parser.AngleCalculatorParameters as param

EXPORT_PDOA = True

dataFolderPath = "../src/data"
if not os.path.exists(dataFolderPath+"/"+"figures"):
    os.makedirs(dataFolderPath+"/"+"figures")

dataName = "20211112_1230120p024_2mOfficial2"
usedPairs = [0, 1, 5]

if not os.path.exists(dataFolderPath+"/"+"figures"+"/"+dataName):
    os.makedirs(dataFolderPath+"/"+"figures"+"/"+dataName)
figureFolderPath = dataFolderPath+"/"+"figures"+"/"+dataName
#extract data from CSV
dataCsv = pd.read_csv(dataFolderPath + "/"+ dataName + '.csv')
data = parse.remAnormalRx(dataCsv)
dataBundled, angles = parse.bundle(data)

dPDOA = compute.PDOA(dataBundled,[data.columns.values[[3,7,11]]],[data.columns.values[[4,8,12]]],angles)
mdPDOA,sdPDOA = compute.stats(dPDOA)

PDOAscaleFactor = {}
for nb in usedPairs:
    PDOAscaleFactor["PDOA"+str(nb)] = p.extractSlopeExtremums(dPDOA,mdPDOA,namePDOA="PDOA"+str(nb))

PDOAscaleFactor["PDOA2"]=0
PDOAscaleFactor["PDOA3"]=0
PDOAscaleFactor["PDOA4"]=0
# recompute PDOA with centering (skew correction)
dPDOA = compute.PDOA(dataBundled,[data.columns.values[[3,7,11]]],[data.columns.values[[4,8,12]]],angles,offset=PDOAscaleFactor)
mdPDOA,sdPDOA = compute.stats(dPDOA)

for nb in usedPairs:
    p.plotPDOA(dPDOA,mdPDOA,sdPDOA,namePDOA='PDOA'+str(nb))
# confusion zone
for line in [30, 90]:
    plt.plot([0,360],[-line,-line],"--r")
    plt.plot([0,360],[line,line],"--r")
plt.show()

# export angle calculator parameters to pickle format
if EXPORT_PDOA:
    PDOAlineFit = {}
    for nb in usedPairs:
        tempDic = p.extractSlopes(dPDOA, mdPDOA, namePDOA="PDOA" + str(nb))
        PDOAlineFit.update(tempDic)

    exporter = export.Exporter(dataFolderPath)
    pairs = {}
    for n in usedPairs:
        pairs["PDOA" + str(n)] = param.AngleCalculatorParameters()
        pairs["PDOA" + str(n)].m_pairID = n

    export.setPdoaSlopesCarac(pairs, PDOAlineFit, PDOAscaleFactor)
    export.setAntennaPairs(pairs)

    exporter.toPickle(pairs)
