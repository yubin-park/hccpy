
def get_risk_dct(coefn, hcc_lst, age, sex):

    risk_dct = {}

    # build demographic bracket strings and add to risk_dct
    # NOTE: Need modifications to classify New Enrollees in the future
    # NOTE: Functioning Graft model not included as well. Need improvement.
    elig_demo = "DI_" # dialysis status
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
    
    # build hcc factor strings and add to risk_dict
    for hcc in hcc_lst:
        elig_hcc = "DI_" + hcc
        risk_dct[elig_hcc] = coefn.get(elig_hcc, 0.0)

    return risk_dct


