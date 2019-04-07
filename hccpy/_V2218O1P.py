
def get_risk_dct(coefn, hcc_lst, age, sex, elig, origds):

    risk_dct = {}

    # demographic factors

    elig_demo = elig 
    if elig[:3] in {"CFA", "CFD", "CNA", "CND", "CPA", "CPD", "INS"}:
        elig_demo += "_" 
    elig_demo += sex

    age_ranges = [x for x in coefn if elig_demo in x]
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
    if age_match in coefn:
        risk_dct[age_match] = coefn[age_match]

    if origds > 0:
        elig_origds = elig + "_OriginallyDisabled_"
        if sex == "M":
            elig_origds += "Male" 
        else:
            elig_origds += "Femle" 
        if elig_origds in coefn:
            risk_dct[elig_origds] = coefn[elig_origds]

    # hcc factors
    for hcc in hcc_lst:
        elig_hcc = elig + "_" + hcc
        if elig_hcc in coefn:
            risk_dct[elig_hcc] = coefn[elig_hcc]

    return risk_dct


