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
    z["CANCER"] = max(x["HCC17"], x["HCC18"], x["HCC19"], 
                        x["HCC20"], x["HCC21"], x["HCC22"], x["HCC23"])
    z["DIABETES"] = max(x["HCC35"], x["HCC36"], x["HCC37"], x["HCC38"])
    z["CARD_RESP_FAIL"] = max(x["HCC211"], x["HCC212"], x["HCC213"])
    z["HF"] = max(x["HCC221"], x["HCC222"], x["HCC223"], 
                x["HCC224"], x["HCC225"], x["HCC226"])
    z["CHR_LUNG"] = max(x["HCC276"], x["HCC277"], x["HCC278"], 
                        x["HCC279"], x["HCC280"])
    z["KIDNEY"] = max(x["HCC326"], x["HCC327"], x["HCC328"], x["HCC329"])
    z["SEPSIS"] = x["HCC2"]
    z["gSubUseDisorder"] = max(x["HCC135"], x["HCC136"], x["HCC137"],
                            x["HCC138"], x["HCC139"])
    z["gPsychiatric"] =  max(x["HCC151"], x["HCC152"], 
                                x["HCC153"], x["HCC154"], x["HCC155"])
    z["NEURO"] = max(x["HCC180"], x["HCC181"], x["HCC182"], 
                        x["HCC190"], x["HCC191"], x["HCC192"],
                        x["HCC195"], x["HCC196"], x["HCC198"],
                        x["HCC199"])
    z["ULCER"] = max(x["HCC379"], x["HCC380"], x["HCC381"], x["HCC382"]) 

    # community model interactions
    # NOTE: updated interaction codes to match V24hcccoefn.csv; values changed from V23 --> V24
    x["DIABETES_HF"] = z["DIABETES"] * z["HF"]
    x["HF_CHR_LUNG"] = z["HF"] * z["CHR_LUNG"]
    x["HF_KIDNEY"] = z["HF"] * z["KIDNEY"]
    x["CHR_LUNG_CARD_RESP_FAIL"] = z["CHR_LUNG"] * z["CARD_RESP_FAIL"]
    x["HF_HCC238"] = z["HF"] * x["HCC238"]
    x["gSubUseDisorder_gPsych"] = (z["gSubUseDisorder"] *
                                        z["gPsychiatric"])
    
    # institutional model interactions
    x["DISABLED_CANCER"] = DISABL * z["CANCER"]
    x["DISABLED_NEURO"] = DISABL * z["NEURO"]
    x["DISABLED_HF"] = DISABL * z["HF"]
    x["DISABLED_CHR_LUNG"] = DISABL * z["CHR_LUNG"]
    x["DISABLED_ULCER"] = DISABL * z["ULCER"]

    cc_lst = [k for k, v in x.items() if v > 0]

    return cc_lst


