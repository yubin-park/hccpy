from collections import Counter

def _adult(cc_lst):

    x = Counter(cc_lst)
    z = Counter()

    if (x["HHS_HCC002"] + x["HHS_HCC042"] + x["HHS_HCC120"] + 
        x["HHS_HCC122"] + x["HHS_HCC125"] + x["HHS_HCC126"] +
        x["HHS_HCC127"] + x["HHS_HCC156"]):
        z["SEVERE_V3"] = 1

    gvarmap = {"G01": ["HHS_HCC019", "HHS_HCC020", "HHS_HCC021"],
            "G02A": ["HHS_HCC026", "HHS_HCC027", 
                        "HHS_HCC029", "HHS_HCC030"],
            "G03": ["HHS_HCC054", "HHS_HCC055"],
            "G04": ["HHS_HCC061", "HHS_HCC062"],
            "G06": ["HHS_HCC067", "HHS_HCC068"],
            "G07": ["HHS_HCC069", "HHS_HCC070", "HHS_HCC071"],
            "G08": ["HHS_HCC073", "HHS_HCC074"],
            "G09": ["HHS_HCC081", "HHS_HCC082"],
            "G10": ["HHS_HCC106", "HHS_HCC107"],
            "G11": ["HHS_HCC108", "HHS_HCC109"],
            "G12": ["HHS_HCC117", "HHS_HCC119"],
            "G13": ["HHS_HCC126", "HHS_HCC127"],
            "G14": ["HHS_HCC128", "HHS_HCC129"],
            "G15": ["HHS_HCC160", "HHS_HCC161"],
            "G16": ["HHS_HCC187", "HHS_HCC188"],
            "G17": ["HHS_HCC203", "HHS_HCC204", "HHS_HCC205"],
            "G18": ["HHS_HCC207", "HHS_HCC208", "HHS_HCC209"]}
    for gvar, cc_lst in gvarmap.items():
        for cc in cc_lst:
            if x[cc] > 0:
                x[gvar] = 1
                x[cc] = 0
    
    # Severe illness interactions 
    z["SEVERE_V3_x_HHS_HCC006"] = z["SEVERE_V3"] * x["HHS_HCC006"]
    z["SEVERE_V3_x_HHS_HCC008"] = z["SEVERE_V3"] * x["HHS_HCC008"]
    z["SEVERE_V3_x_HHS_HCC009"] = z["SEVERE_V3"] * x["HHS_HCC009"]
    z["SEVERE_V3_x_HHS_HCC010"] = z["SEVERE_V3"] * x["HHS_HCC010"]
    z["SEVERE_V3_x_HHS_HCC115"] = z["SEVERE_V3"] * x["HHS_HCC115"]
    z["SEVERE_V3_x_HHS_HCC135"] = z["SEVERE_V3"] * x["HHS_HCC135"]
    z["SEVERE_V3_x_HHS_HCC145"] = z["SEVERE_V3"] * x["HHS_HCC145"]
    z["SEVERE_V3_x_G06"]        = z["SEVERE_V3"] * x["G06"];
    z["SEVERE_V3_x_G08"]        = z["SEVERE_V3"] * x["G08"];

    z["SEVERE_V3_x_HHS_HCC035"] = z["SEVERE_V3"] * x["HHS_HCC035"]
    z["SEVERE_V3_x_HHS_HCC038"] = z["SEVERE_V3"] * x["HHS_HCC038"]
    z["SEVERE_V3_x_HHS_HCC153"] = z["SEVERE_V3"] * x["HHS_HCC153"]
    z["SEVERE_V3_x_HHS_HCC154"] = z["SEVERE_V3"] * x["HHS_HCC154"]
    z["SEVERE_V3_x_HHS_HCC163"] = z["SEVERE_V3"] * x["HHS_HCC163"]
    z["SEVERE_V3_x_HHS_HCC253"] = z["SEVERE_V3"] * x["HHS_HCC253"]
    z["SEVERE_V3_x_G03"]        = z["SEVERE_V3"] * x["G03"];

    if (z["SEVERE_V3_x_HHS_HCC006"] + z["SEVERE_V3_x_HHS_HCC008"] +
        z["SEVERE_V3_x_HHS_HCC009"] + z["SEVERE_V3_x_HHS_HCC010"] +
        z["SEVERE_V3_x_HHS_HCC115"] + z["SEVERE_V3_x_HHS_HCC135"] +
        z["SEVERE_V3_x_HHS_HCC145"] + z["SEVERE_V3_x_G06"] +
        z["SEVERE_V3_x_G08"]):
        x["INT_GROUP_H"] = 1
    
    if (z["SEVERE_V3_x_HHS_HCC035"] + z["SEVERE_V3_x_HHS_HCC038"] +
        z["SEVERE_V3_x_HHS_HCC153"] + z["SEVERE_V3_x_HHS_HCC154"] +
        z["SEVERE_V3_x_HHS_HCC163"] + z["SEVERE_V3_x_HHS_HCC253"] +
        z["SEVERE_V3_x_G03"]):
        x["INT_GROUP_M"] = 1

    # NOTE: ED variables are ignored in this library
    for i in range(1, 12):
        x["ED_{}".format(i)] = 1

    x["RXC_01_X_HCC001"] = x["RXC_01"] * x["HHS_HCC001"]
    x["RXC_02_X_HCC037_1_036_035_034"] = (x["RXC_02"] *
                (x["HHS_HCC034"] + x["HHS_HCC035"] + x["HHS_HCC036"] +
                    x["HHS_HCC037_1"]))
    x["RXC_03_X_HCC142"] = x["RXC_03"] * x["HHS_HCC142"]
    x["RXC_04_X_HCC184_183_187_188"] = (x["RXC_04"] *
                (x["HHS_HCC184"] + x["HHS_HCC183"] + x["HHS_HCC187"] + 
                    x["HHS_HCC188"]))
    x["RXC_05_X_HCC048_041"] = (x["RXC_05"] * (x["HHS_HCC048"] + 
                                    x["HHS_HCC041"]))
    x["RXC_06_X_HCC018_019_020_021"] = (x["RXC_06"] * 
                (x["HHS_HCC018"] + x["HHS_HCC019"] + x["HHS_HCC020"] + 
                    x["HHS_HCC021"]))
    x["RXC_07_X_HCC018_019_020_021"] = (x["RXC_07"] * 
                (x["HHS_HCC018"] + x["HHS_HCC019"] + x["HHS_HCC020"] + 
                    x["HHS_HCC021"]))
    x["RXC_08_X_HCC118"] = x["RXC_08"] * x["HHS_HCC118"]
    x["RXC_09_X_HCC056_057_AND_048_041"] = (x["RXC_09"] *
                (x["HHS_HCC056"] + x["HHS_HCC057"]) * 
                (x["HHS_HCC048"] + x["HHS_HCC041"]))
    x["RXC_09_X_HCC056"] = x["RXC_09"] * x["HHS_HCC056"]
    x["RXC_09_X_HCC057"] = x["RXC_09"] * x["HHS_HCC057"]
    x["RXC_09_X_HCC048_041"] = (x["RXC_09"] * (x["HHS_HCC048"] + 
                                x["HHS_HCC041"]))
    x["RXC_10_X_HCC159_158"] = (x["RXC_10"] * (x["HHS_HCC159"] + 
                                x["HHS_HCC158"]))

    cc_lst = [k for k, v in x.items() if v > 0]

    return cc_lst
   
   
def _child(cc_lst):
    pass

def _infant(cc_lst):
    pass


def create_interactions(cc_lst, agegroup):
    
    cc_lst = cc_lst
    if agegroup == "Adult":
        cc_lst = _adult(cc_lst)
    elif agegroup == "Child":
        cc_lst = _child(cc_lst)
    elif agegroup == "Infant":
        cc_lst = _infant(cc_lst)

    return cc_lst


