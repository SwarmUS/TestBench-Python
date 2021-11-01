# Structure containing all parameters used to calculate an angle. These parameters are calculated
# using the Python tooling during calibration and then transferred to the board.

class AngleCalculatorParameters:
    def __init__(self):
        pass
    m_pairID = None
    # Normalization factors used to stretch TDOA angles between - 90 and +90 degrees.(Applied by
    # dividing by the normalization before applying the asin() on the TDOA)
    m_tdoaNormalizationFactors = None

    # Slopes (a in y = ax + b) of the non - reciprocated TDOA functions(calculatedAngle=a * realAngle + b)
    m_tdoaSlopes = None

    # Intercepts(b in y = ax + b) of the non - reciprocated TDOA functions \
    # (calculatedAngle = a * realAngle+b)
    m_tdoaIntercepts = None

    # Normalization factors used to stretch PDOA angles between -90 and +90 degrees. (Applied by
    # dividing by the normalization after applying the asin() on the PDOA)
    m_pdoaNormalizationFactors = None

    # Slopes (a in y=ax+b) of the non-reciprocated PDOA functions (calculatedAngle = a*realAngle+b)
    # A single (positive) slope is used for all PDOA curves. The sign of the slope is applied at
    # runtime.\
    m_pdoaSlopes = None

    # Intercepts (b in y=ax+b) of the non-reciprocated PDOA functions for every curve
    # (calculatedAngle = a*realAngle+b)
    m_pdoaIntercepts = None

    # Origins (value for angle=-90 degrees) for every PDOA curve. Used to decide which curve to use
    m_pdoaOrigins = None

    # Lookup table used to know which antenna IDs are used in each pair ID
    # TDOAx = m_antennaPairs[0]-m_antennaPairs[1]
    m_antennaPairs = None
