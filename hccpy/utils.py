import csv
import re
from pkg_resources import resource_filename

def read_dx2cc(fn):
    dx2cc = {}
    fn = resource_filename(__name__, fn)
    with open(fn, "r") as fp:
        reader = csv.reader(fp, delimiter="\t")
        dx2cc = {x[0].strip(): "HCC"+x[1].strip() for x in reader}
    return dx2cc

def read_coefn(fn):
    coef = {}
    fn = resource_filename(__name__, fn)
    with open(fn, "r") as fp:
        reader = csv.reader(fp, delimiter=",")
        header = next(reader)
        values = [float(x) for x in next(reader)]
        coef = {k.strip(): v for k, v in zip(header, values)}
    return coef

def read_hier(fn):
    hiers = {}
    pttr = r"%SET0\(CC=(\d+).+%STR\((.+)\)\)"
    fn = resource_filename(__name__, fn)
    with open(fn, "r") as fp:
        for line in fp.readlines(): 
            matches = re.findall(pttr, line)
            if len(matches) < 1 or len(matches[0]) < 2:
                continue
            k = "HCC"+str(matches[0][0])
            v = ["HCC"+x.strip() for x in matches[0][1].split(",")]
            hiers[k] = v 
    return hiers 

def read_label(fn):
    labels = {}
    pttr = r"HCC(\d+)\s+=\"(.+)\""
    fn = resource_filename(__name__, fn)
    with open(fn, "r") as fp:
        for line in fp.readlines(): 
            matches = re.findall(pttr, line)
            if len(matches) < 1 or len(matches[0]) < 2:
                continue
            k = str(matches[0][0])
            v = matches[0][1].strip()
            labels[k] = v 
    return labels




