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
    z["IMMUNE"] = x["HCC47"]
    z["CARD_RESP_FAIL"] = max(x["HCC82"], x["HCC83"], x["HCC84"])
    z["CHF"] = x["HCC85"]
    z["COPD"] = max(x["HCC110"], x["HCC111"])
    z["RENAL"] = max(x["HCC134"], x["HCC135"], x["HCC136"], 
                            x["HCC137"], x["HCC138"], x["HCC139"],
                            x["HCC140"], x["HCC141"])
    z["COMPL"] = x["HCC176"]
    z["SEPSIS"] = x["HCC2"]

    # community model interactions
    x["SEPSIS_CARD_RESP_FAIL"] =  z["SEPSIS"] * z["CARD_RESP_FAIL"]
    x["CANCER_IMMUNE"] = z["CANCER"] * z["IMMUNE"]
    x["DIABETES_CHF"] = z["DIABETES"] * z["CHF"]
    x["CHF_COPD"] = z["CHF"] * z["COPD"]
    x["CHF_RENAL"] = z["CHF"] * z["RENAL"]
    x["COPD_CARD_RESP_FAIL"] = z["COPD"] * z["CARD_RESP_FAIL"]
    
    # institutional model interactions
    x["NONAGED_HCC6"] = DISABL * x["HCC6"]
    x["NONAGED_HCC34"] = DISABL * x["HCC34"]
    x["NONAGED_HCC46"] = DISABL * x["HCC46"]
    x["NONAGED_HCC54"]  = DISABL * x["HCC54"]
    x["NONAGED_HCC55"]  = DISABL * x["HCC55"]
    x["NONAGED_HCC110"] = DISABL * x["HCC110"]
    x["NONAGED_HCC176"] = DISABL * x["HCC176"]

    x["PRESSURE_ULCER"] = max(x["HCC157"], x["HCC158"], 
                            x["HCC159"], x["HCC160"])
    x["SEPSIS_PRESSURE_ULCER"] = z["SEPSIS"] * x["PRESSURE_ULCER"]
    x["SEPSIS_ARTIF_OPENINGS"] = z["SEPSIS"] * x["HCC188"]
    x["ART_OPENINGS_PRESSURE_ULCER"] = x["HCC188"] * x["PRESSURE_ULCER"]
    x["DIABETES_CHF"] = z["DIABETES"] * z["CHF"]
    x["COPD_ASP_SPEC_BACT_PNEUM"] = z["COPD"] * x["HCC114"]
    x["ASP_SPEC_BACT_PNEUM_PRES_ULC"] = x["HCC114"] * x["PRESSURE_ULCER"]
    x["SEPSIS_ASP_SPEC_BACT_PNEUM"] = z["SEPSIS"] * x["HCC114"]
    x["SCHIZOPHRENIA_COPD"] = x["HCC57"] * z["COPD"]
    x["SCHIZOPHRENIA_CHF"] = x["HCC57"] * z["CHF"]
    x["SCHIZOPHRENIA_SEIZURES"] = x["HCC57"] * x["HCC79"]

    x["NONAGED_HCC85"] = DISABL * x["HCC85"]
    x["NONAGED_PRESSURE_ULCER"] = DISABL * x["PRESSURE_ULCER"]
    x["NONAGED_HCC161"] = DISABL * x["HCC161"]
    x["NONAGED_HCC39"] = DISABL * x["HCC39"]
    x["NONAGED_HCC77"] = DISABL * x["HCC77"]

    cc_lst = [k for k, v in x.items() if v > 0]

    return cc_lst


