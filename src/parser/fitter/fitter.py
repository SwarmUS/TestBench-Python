
import src.parser.fitter.fitter_functions as f

def findPhaseReverse(mPDOA):
    return f.findMin(f.filterLP(f.diff(mPDOA)))

#get the distance between 2*pi and the sin maxsor mins
def offsetPDOA(mdPDOA):
    return f.offset(mdPDOA)

