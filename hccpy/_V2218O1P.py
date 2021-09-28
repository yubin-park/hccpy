
def get_risk_dct(coefn, hcc_lst, age, sex, elig, origds, medicaid):

    risk_dct = {}

    # build demographic bracket strings and add to risk_dct
    elig_demo = elig 
    if elig[:3] in {"CFA", "CFD", "CNA", "CND", "CPA", "CPD", "INS"}:
        elig_demo += "_" 
    elig_demo += sex

    # build age bracket strings and add to risk_dct
    age_ranges = [x for x in coefn.keys() if elig_demo in x]
    age_match = ""
    for age_range in age_ranges:
        age_tokens = age_range.replace(elig_demo, "").split("_") 
        lb, ub = 0, 999 
        if len(age_tokens) == 1:
            lb = int(age_tokens[0])
            ub = lb + 1
        elif age_tokens[1] == "GT":
            lb = int(age_tokens[0])
        else: 
            lb = int(age_tokens[0])
            ub = int(age_tokens[1]) + 1
        if lb <= age < ub:
            age_match = age_range
            break
    risk_dct[age_match] = coefn.get(age_match, 0.0)
    
    # build original entitlement string and add to risk_dct
    if origds > 0:
        elig_origds = elig + "_OriginallyDisabled_"
        if sex == "M":
            elig_origds += "Male" 
        else:
            elig_origds += "Female"     
        risk_dct[elig_origds] = coefn.get(elig_origds, 0.0)
    
    # build medicaid interacion and add to risk_dict
    if medicaid:
        mcd_hcc = elig + "_" + "LTIMCAID"
        risk_dct[mcd_hcc] = coefn.get(mcd_hcc, 0.0)

    # build hcc factor strings and add to risk_dict
    for hcc in hcc_lst:
        elig_hcc = elig + "_" + hcc
        risk_dct[elig_hcc] = coefn.get(elig_hcc, 0.0)

    return risk_dct


