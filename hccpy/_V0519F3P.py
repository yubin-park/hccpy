
def get_risk_dct(coefn, hcc_lst, agesexvar, agegroup, plate):

    risk_dct = {}

    if agegroup+"_"+agesexvar in coefn:
        risk_dct[agesexvar] = coefn[agegroup+"_"+agesexvar][plate]

    for hcc in hcc_lst:
        if agegroup+"_"+hcc in coefn:
            risk_dct[hcc] = coefn[agegroup+"_"+hcc][plate]

    return risk_dct


