def mapDict(fct, d,params0=None,params1=None):
    if params0 == None and params1 == None:
        return {k: fct(v) for k, v in d.items()}
    elif params0 != None and params1 == None:
        return {k: fct(v,params0[k]) for k, v in d.items()}
    else:
        return {k: fct(v, params0[k],params1[k]) for k, v in d.items()}

def PDtoTD(phaseReverse):
    out = {}
    for k in phaseReverse.keys():
        k1=k.replace("P","T",1)
        out[k1]= phaseReverse[k]

    return out

def TDtoPD(phaseReverse):
    out = {}
    for k in phaseReverse.keys():
        k1=k.replace("T","P",1)
        out[k1]= phaseReverse[k]

    return out
