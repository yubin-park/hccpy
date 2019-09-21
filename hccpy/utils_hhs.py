import csv
import re
from pkg_resources import resource_filename as rscfn

def padded_cc(cc):
    cc = cc.replace(".","_")
    pz = "".join(["0"] *(3-len(cc.split("_")[0])))
    return "{}{}".format(pz, cc)

def read_dx2cc(fn):
    dx2cc = {}
    fn = rscfn(__name__, fn)
    with open(fn, "r") as fp:
        reader = csv.reader(fp, delimiter="\t")
        for row in reader:
            row = [x.strip() for x in row]
            cc = padded_cc(row[1])
            dx2cc[row[0]] = "HHS_HCC{}".format(cc)
    return dx2cc

def read_code2rxc(fn):
    code2rxc = {}
    fn = rscfn(__name__, fn)
    with open(fn, "r") as fp:
        reader = csv.reader(fp, delimiter="\t")
        for row in reader:
            row = [x.strip() for x in row]
            pz = "".join(["0"] *(2-len(row[1])))
            rxc = "RXC{}{}".format(pz, row[1])
            code2rxc[row[0]] = rxc
            rxclabels[rxc] = row[2]
    return code2rxc

def read_coefn(fn):
    coef = {}
    fn = rscfn(__name__, fn)
    with open(fn, "r") as fp:
        reader = csv.reader(fp, delimiter=",")
        header = next(reader)
        for row in reader:
            row = [x.strip() for x in row]
            if row[0] == "":
                continue
            agegrp = row[0]
            varname = row[1]
            values = {"P": float(row[3]),
                    "G": float(row[4]),
                    "S": float(row[5]),
                    "B": float(row[6]),
                    "C": float(row[7])}
            coef[agegrp+"_"+varname] = values
    return coef

def read_hier(fn):
    hiers = {}
    pttr = r"%SET0\(CC=(\d+.?\d?).+%STR\((.+)\)\)"
    fn = rscfn(__name__, fn)
    with open(fn, "r") as fp:
        for line in fp.readlines(): 
            matches = re.findall(pttr, line)
            if len(matches) < 1 or len(matches[0]) < 2:
                continue
            k = "HHS_HCC"+padded_cc(matches[0][0].strip())
            v = ["HHS_HCC"+padded_cc(x.strip()) 
                    for x in matches[0][1].split(",")]
            hiers[k] = v 
    return hiers 

def read_label(fn):
    labels = {}
    pttr = r"(HHS_HCC|HHS_CC|RXC_)(\d+.?\d?)\s?=\"(.+)\""
    fn = rscfn(__name__, fn)
    with open(fn, "r") as fp:
        for line in fp.readlines(): 
            matches = re.findall(pttr, line)
            if len(matches) < 1 or len(matches[0]) < 2:
                continue
            k = matches[0][0] + matches[0][1].strip()
            v = matches[0][2].strip()
            labels[k] = v 
    return labels

#if __name__ == "__main__":

    #data = read_dx2cc("data/H0519F3.FY 2019 ICD10.TXT")
    #print(data)
    #ndc2rxc = read_code2rxc("data/H0519F3_NDC.4_4.1812.TXT")
    #print(ndc2rxc)
    #hcpcs2rxc = read_code2rxc("data/H0519F3_HCPCS.4_4.1812.TXT")
    #print(hcpcs2rxc)

    #hier = read_hier("data/V05128H1.TXT")
    #print(hier)
    #labels = read_label("data/V05128L1.TXT")
    #import json
    #print(json.dumps(labels, indent=2, sort_keys=True))

    #coefn = read_coefn("data/HHS19hcccoefn.csv")
    #print(coefn)
