from collections import Counter
import numpy as np

def _adult(cc_lst):

    x = Counter(cc_lst)
    z = Counter()

    # Mandatory for adults
    x["HHS_HCC028"] = 0
    x["HHS_HCC064"] = 0
    x["HHS_HCC137"] = 0
    x["HHS_HCC138"] = 0
    x["HHS_HCC139"] = 0
    x["HHS_HCC242"] = 0
    x["HHS_HCC243"] = 0
    x["HHS_HCC244"] = 0
    x["HHS_HCC245"] = 0
    x["HHS_HCC246"] = 0
    x["HHS_HCC247"] = 0
    x["HHS_HCC248"] = 0
    x["HHS_HCC249"] = 0

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
    #for i in range(1, 12):
    #    x["ED_{}".format(i)] = 1

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
 
    x = Counter(cc_lst)
    z = Counter()

    # Mandatory for children
    x["HHS_HCC064"] = 0
    x["HHS_HCC242"] = 0
    x["HHS_HCC243"] = 0
    x["HHS_HCC244"] = 0
    x["HHS_HCC245"] = 0
    x["HHS_HCC246"] = 0
    x["HHS_HCC247"] = 0
    x["HHS_HCC248"] = 0
    x["HHS_HCC249"] = 0
   
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

    cc_lst = [k for k, v in x.items() if v > 0]

    return cc_lst

def _infant(cc_lst, age):

    x = Counter(cc_lst)
    z = Counter()

    # Mandatory for infants 
    x["HHS_HCC087"] = 0
    x["HHS_HCC088"] = 0
    x["HHS_HCC089"] = 0
    x["HHS_HCC090"] = 0
    x["HHS_HCC094"] = 0
    x["HHS_HCC203"] = 0
    x["HHS_HCC204"] = 0
    x["HHS_HCC205"] = 0
    x["HHS_HCC207"] = 0
    x["HHS_HCC208"] = 0
    x["HHS_HCC209"] = 0

    svarmap = {"IHCC_Severity5": ["HHS_HCC008", "HHS_HCC018",
                    "HHS_HCC034", "HHS_HCC035", "HHS_HCC041",
                    "HHS_HCC042", "HHS_HCC125", "HHS_HCC128",
                    "HHS_HCC129", "HHS_HCC130", "HHS_HCC137",
                    "HHS_HCC158", "HHS_HCC183", "HHS_HCC184",
                    "HHS_HCC251"],
                "IHCC_Severity4": ["HHS_HCC002", "HHS_HCC009"
                    "HHS_HCC026", "HHS_HCC064", "HHS_HCC067",
                    "HHS_HCC068", "HHS_HCC073", "HHS_HCC106", 
                    "HHS_HCC107", "HHS_HCC111", "HHS_HCC112",
                    "HHS_HCC115", "HHS_HCC122", "HHS_HCC126",
                    "HHS_HCC127", "HHS_HCC131", "HHS_HCC135",
                    "HHS_HCC138", "HHS_HCC145", "HHS_HCC146",
                    "HHS_HCC154", "HHS_HCC156", "HHS_HCC163",
                    "HHS_HCC187", "HHS_HCC226", "HHS_HCC253"],
                "IHCC_Severity3": ["HHS_HCC001", "HHS_HCC003",
                    "HHS_HCC006", "HHS_HCC010", "HHS_HCC011",
                    "HHS_HCC012", "HHS_HCC027", "HHS_HCC030",
                    "HHS_HCC038", "HHS_HCC045", "HHS_HCC054",
                    "HHS_HCC055", "HHS_HCC061", "HHS_HCC063",
                    "HHS_HCC066", "HHS_HCC074", "HHS_HCC075",
                    "HHS_HCC096", "HHS_HCC108", "HHS_HCC109",
                    "HHS_HCC110", "HHS_HCC113", "HHS_HCC117",
                    "HHS_HCC119", "HHS_HCC121", "HHS_HCC132",
                    "HHS_HCC139", "HHS_HCC142", "HHS_HCC149",
                    "HHS_HCC150", "HHS_HCC159", "HHS_HCC162",
                    "HHS_HCC227"],
                "IHCC_Severity2": ["HHS_HCC004", "HHS_HCC013",
                    "HHS_HCC019", "HHS_HCC020", "HHS_HCC021",
                    "HHS_HCC023", "HHS_HCC028", "HHS_HCC029",
                    "HHS_HCC036", "HHS_HCC046", "HHS_HCC048",
                    "HHS_HCC056", "HHS_HCC057", "HHS_HCC062",
                    "HHS_HCC069", "HHS_HCC070", "HHS_HCC081",
                    "HHS_HCC082", "HHS_HCC097", "HHS_HCC114",
                    "HHS_HCC120", "HHS_HCC151", "HHS_HCC153",
                    "HHS_HCC160", "HHS_HCC217"],
                "IHCC_Severity1": ["HHS_HCC037_1", "HHS_HCC037_2",
                    "HHS_HCC047", "HHS_HCC071", "HHS_HCC102",
                    "HHS_HCC103", "HHS_HCC118", "HHS_HCC161",
                    "HHS_HCC188", "HHS_HCC254"]}
    
    for svar, cc_lst in svarmap.items():
        for cc in cc_lst:
            if x[cc] > 0:
                z[svar] = 1
                x[cc] = 0

    for i in reversed(range(2, 6)):
        if z["IHCC_Severity{}".format(i)] > 0:
            for j in range(1, i):
                z["IHCC_Severity{}".format(j)] = 0
    if np.sum(z.values()) == 0:
        z["IHCC_Severity1"] = 1

    if age >=1:
        z["IHCC_Age1"] = 1
    else:
        z["IHCC_Extremely_Immature"] = (x["HHS_HCC242"] + 
                x["HHS_HCC243"] + x["HHS_HCC244"])
        z["IHCC_Immature"] = x["HHS_HCC245"] + x["HHS_HCC246"]
        z["IHCC_Premature_Multiples"] = x["HHS_HCC247"] + x["HHS_HCC248"]
        z["IHCC_Term"] = x["HHS_HCC249"]
        if (x["HHS_HCC242"] + x["HHS_HCC243"] + x["HHS_HCC244"] + 
            x["HHS_HCC245"] + x["HHS_HCC246"] + x["HHS_HCC247"] + 
            x["HHS_HCC248"] + x["HHS_HCC249"] == 0):
            z["IHCC_AGE1"] = 1
        if z["IHCC_Extremely_Immature"] > 0:
            z["IHCC_Immature"] = 0
            z["IHCC_Premature_Multiples"] = 0
            z["IHCC_Term"] = 0
            z["IHCC_AGE1"] = 0
        elif z["IHCC_Immature"] > 0:
            z["IHCC_Premature_Multiples"] = 0
            z["IHCC_Term"] = 0
            z["IHCC_AGE1"] = 0
        elif z["IHCC_Premature_Multiples"] > 0:
            z["IHCC_Term"] = 0
            z["IHCC_AGE1"] = 0
        elif z["IHCC_Term"] > 0:
            z["IHCC_AGE1"] = 0

    # NOTE: age/sex re-assignment is ignored
 
    x["EXTREMELY_IMMATURE_X_SEVERITY5"] = z["IHCC_Severity5"] * z["IHCC_Extremely_Immature"]
    x["IMMATURE_X_SEVERITY5"] = z["IHCC_Severity5"] * z["IHCC_Immature"]
    x["PREMATURE_MULTIPLES_X_SEVERITY5"] = z["IHCC_Severity5"] * z["IHCC_Premature_Multiples"]
    x["TERM_X_SEVERITY5"] = z["IHCC_Severity5"] * z["IHCC_Term"]
    x["AGE1_X_SEVERITY5"] = z["IHCC_Severity5"] * z["IHCC_Age1"]
    x["EXTREMELY_IMMATURE_X_SEVERITY4"] = z["IHCC_Severity4"] * z["IHCC_Extremely_Immature"]
    x["IMMATURE_X_SEVERITY4"] = z["IHCC_Severity4"] * z["IHCC_Immature"]
    x["PREMATURE_MULTIPLES_X_SEVERITY4"] = z["IHCC_Severity4"] * z["IHCC_Premature_Multiples"]
    x["TERM_X_SEVERITY4"] = z["IHCC_Severity4"] * z["IHCC_Term"]
    x["AGE1_X_SEVERITY4"] = z["IHCC_Severity4"] * z["IHCC_Age1"]
    x["EXTREMELY_IMMATURE_X_SEVERITY3"] = z["IHCC_Severity3"] * z["IHCC_Extremely_Immature"]
    x["IMMATURE_X_SEVERITY3"] = z["IHCC_Severity3"] * z["IHCC_Immature"]
    x["PREMATURE_MULTIPLES_X_SEVERITY3"] = z["IHCC_Severity3"] * z["IHCC_Premature_Multiples"]
    x["TERM_X_SEVERITY3"] = z["IHCC_Severity3"] * z["IHCC_Term"]
    x["AGE1_X_SEVERITY3"] = z["IHCC_Severity3"] * z["IHCC_Age1"]
    x["EXTREMELY_IMMATURE_X_SEVERITY2"] = z["IHCC_Severity2"] * z["IHCC_Extremely_Immature"]
    x["IMMATURE_X_SEVERITY2"] = z["IHCC_Severity2"] * z["IHCC_Immature"]
    x["PREMATURE_MULTIPLES_X_SEVERITY2"] = z["IHCC_Severity2"] * z["IHCC_Premature_Multiples"]
    x["TERM_X_SEVERITY2"] = z["IHCC_Severity2"] * z["IHCC_Term"]
    x["AGE1_X_SEVERITY2"] = z["IHCC_Severity2"] * z["IHCC_Age1"]
    x["EXTREMELY_IMMATURE_X_SEVERITY1"] = z["IHCC_Severity1"] * z["IHCC_Extremely_Immature"]
    x["IMMATURE_X_SEVERITY1"] = z["IHCC_Severity1"] * z["IHCC_Immature"]
    x["PREMATURE_MULTIPLES_X_SEVERITY1"] = z["IHCC_Severity1"] * z["IHCC_Premature_Multiples"]
    x["TERM_X_SEVERITY1"] = z["IHCC_Severity1"] * z["IHCC_Term"]
    x["AGE1_X_SEVERITY1"] = z["IHCC_Severity1"] * z["IHCC_Age1"]

    cc_lst = [k for k, v in x.items() if v > 0]
   
    return cc_lst


def create_interactions(cc_lst, agegroup, age):
    
    cc_lst = cc_lst
    if agegroup == "Adult":
        cc_lst = _adult(cc_lst)
    elif agegroup == "Child":
        cc_lst = _child(cc_lst)
    elif agegroup == "Infant":
        cc_lst = _infant(cc_lst, age)

    return cc_lst


