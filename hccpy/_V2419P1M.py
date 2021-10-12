from collections import Counter

def create_interactions(cc_lst, DISABL, age):
   
    x = Counter(cc_lst) 
    z = Counter()

    # payable HCC's count interaction
    hcccnt = len([k for k in x.keys() if "HCC" in k])
    if hcccnt > 9:
        x["D10P"] = 1
    elif hcccnt > 0:
        x["D{}".format(hcccnt)] = 1

    # diagnostic categories
    z["CANCER"] = max(x["HCC8"], x["HCC9"], x["HCC10"], 
                        x["HCC11"], x["HCC12"])
    z["DIABETES"] = max(x["HCC17"], x["HCC18"], x["HCC19"])
    z["CARD_RESP_FAIL"] = max(x["HCC82"], x["HCC83"], x["HCC84"])
    z["CHF"] = x["HCC85"]
    z["gCopdCF"] = max(x["HCC110"], x["HCC111"], x["HCC112"])
    z["RENAL_V24"] = max(x["HCC134"], x["HCC135"], x["HCC136"], 
                            x["HCC137"], x["HCC138"])
    z["SEPSIS"] = x["HCC2"]
    z["gSubstanceAbuse_V24"] = max(x["HCC54"], x["HCC55"], x["HCC56"])
    z["gPsychiatric_V24"] =  max(x["HCC57"], x["HCC58"], 
                                x["HCC59"], x["HCC60"])

    # community model interactions
    # NOTE: updated interaction codes to match V24hcccoefn.csv; values changed from V23 --> V24
    x["HCC47_gCancer"] = x["HCC47"] * z["CANCER"]
    x["DIABETES_CHF"] = x["HCC85"] * z["DIABETES"]
    x["CHF_gCopdCF"] = x["HCC85"] * z["gCopdCF"]
    x["HCC85_gRenal_V24"] = x["HCC85"] * z["RENAL_V24"]
    x["gCopdCF_CARD_RESP_FAIL"] = z["CARD_RESP_FAIL"] * z["gCopdCF"]
    x["HCC85_HCC96"] = x["HCC85"] * x["HCC96"]
    # x["gSubstanceAbuse_gPsychiatric_V24"] = (z["gPsychiatric_V24"] *
    #                                     z["gSubstanceAbuse_V24"])
    x["gSubstanceUseDisorder_gPsych"] = (z["gPsychiatric_V24"] *
                                        z["gSubstanceAbuse_V24"])
    
    # institutional model interactions
    x["PRESSURE_ULCER"] = max(x["HCC157"], x["HCC158"], x["HCC159"])
    x["SEPSIS_PRESSURE_ULCER"] = z["SEPSIS"] * x["PRESSURE_ULCER"]
    x["SEPSIS_ARTIF_OPENINGS"] = z["SEPSIS"] * x["HCC188"]
    x["ART_OPENINGS_PRESSURE_ULCER"] = x["HCC188"]*x["PRESSURE_ULCER"]
    x["gCopdCF_ASP_SPEC_B_PNEUM"]  = z["gCopdCF"] * x["HCC114"]
    x["ASP_SPEC_BACT_PNEUM_PRES_ULC"] = x["HCC114"]*x["PRESSURE_ULCER"]
    x["SEPSIS_ASP_SPEC_BACT_PNEUM"] = x["SEPSIS"] * x["HCC114"]
    x["SCHIZOPHRENIA_gCopdCF"] = x["HCC57"] * z["gCopdCF"]
    x["SCHIZOPHRENIA_CHF"] = x["HCC57"] * z["CHF"]
    x["SCHIZOPHRENIA_SEIZURES"] = x["HCC57"] * x["HCC79"]

    x["DISABLED_HCC85"] = DISABL * x["HCC85"]
    x["DISABLED_PRESSURE_ULCER"] = DISABL * x["PRESSURE_ULCER"]
    x["DISABLED_HCC161"] = DISABL * x["HCC161"]
    x["DISABLED_HCC39"] = DISABL * x["HCC39"]
    x["DISABLED_HCC77"] = DISABL * x["HCC77"]
    x["DISABLED_HCC6"] = DISABL * x["HCC6"]   

    cc_lst = [k for k, v in x.items() if v > 0]

    return cc_lst


