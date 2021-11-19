# created data bundle for each position of the testBench
def bundle(df):
    angles = df["Angle"].unique()
    dataBundle ={}
    for a in angles:
        subdf = df.loc[df['Angle'] == a]
        flat = flatten(subdf,df.columns.values[[2,3,4, 6,7,8, 10,11,12]])
        dataBundle[a*375/360] = flat

    return dataBundle,angles*375/360

def remAnormalRx(df):
    cdf = df
    # if not the same message on the 3

    # if the TS is anormal
    rxTimestampsCol = df.columns.values[[2, 6, 10]]
    val0 = df[rxTimestampsCol[0]]
    val1 = df[rxTimestampsCol[1]]
    val2= df[rxTimestampsCol[2]]
    tdoaErrVal = 500
    numDrop = 0
    for i in range(0,len(val0)):
        if val0[i]-val1[i] not in range(-tdoaErrVal,tdoaErrVal) or val0[i]-val2[i] not in range(-tdoaErrVal,tdoaErrVal) or val1[i]-val2[i] not in range(-tdoaErrVal,tdoaErrVal):
            cdf = cdf.drop(i-numDrop)
    return cdf


# should remove the clock wrapping
# def remClockWrap(dic):


def flatten (df,columns,x=None):
    flat_dic = {}
    if x is not None:
        for col in columns:
            flat_dic[col]=[]
            for itr in x:
                for item in df[itr][col]:
                        flat_dic[col].append(item)
    else:
        for col in columns:
            flat_dic[col]=[]
            for item in df[col]:
                    flat_dic[col].append(item)
    return flat_dic
