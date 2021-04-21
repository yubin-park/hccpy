
def get_risk_dct(coefn, hcc_lst, agesexvar, agegroup, enroll_dur, plate):

    risk_dct = {}

    if agegroup+"_"+agesexvar in coefn:
        risk_dct[agesexvar] = coefn[agegroup+"_"+agesexvar][plate]
        
    if agegroup+"_"+enroll_dur in coefn:
        risk_dct[enroll_dur] = coefn[agegroup+"_"+enroll_dur][plate]        

    for hcc in hcc_lst:
        if agegroup+"_"+hcc in coefn:
            risk_dct[hcc] = coefn[agegroup+"_"+hcc][plate]

    return risk_dct


