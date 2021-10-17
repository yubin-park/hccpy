import json
import csv
import re
from pkg_resources import resource_filename as rscfn

def read_dx2cc(fn):
    dx2cc = {}
    fn = rscfn(__name__, fn)
    with open(fn, "r") as fp:
        reader = csv.reader(fp, delimiter="\t")
        for x in reader:

            # NOTE: one-to-one mapping was assumed originally
            # NOTE: dx to hcc mapping changes to one-to-many from V24
            # This change will accomodate the mapping
            #dx2cc = {x[0].strip(): "HCC"+x[1].strip() for x in reader}
            
            dx = x[0].strip()
            hcc = "HCC"+x[1].strip()
            if dx not in dx2cc:
                dx2cc[dx] = []
            dx2cc[dx].append(hcc)

    return dx2cc

def read_coefn(fn):
    coef = {}
    fn = rscfn(__name__, fn)
    with open(fn, "r") as fp:
        reader = csv.reader(fp, delimiter=",")
        header = [k.strip() for k in next(reader)]
        values = [float(x) for x in next(reader)]
        coef = {k: v for k, v in zip(header, values)}
    return coef

def read_hier(fn):
    hiers = {}
    pttr = r"%SET0\(CC=(\d+).+%STR\((.+)\)\)"
    fn = rscfn(__name__, fn)
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
    fn = rscfn(__name__, fn)
    with open(fn, "r") as fp:
        for line in fp.readlines(): 
            matches = re.findall(pttr, line)
            if len(matches) < 1 or len(matches[0]) < 2:
                continue
            k = str(matches[0][0])
            v = matches[0][1].strip()
            labels[k] = v 
    return labels

def read_label_short(fn):
    fn = rscfn(__name__, fn)
    label_short = {}
    with open(fn, "r") as fp:
        label_short = json.load(fp)
    return label_short

def combine_dx2cc(file_list, fn):
    """Given file list, read and dedup Dx to HCC mappings. Write to file name"""
    all_lines = []
    all_lines_set = set({})
    for file in file_list:
        with open(file, "r") as f_in:
            for line in f_in.readlines():
                l_strip = line.strip()
                if l_strip not in all_lines_set:
                    all_lines.append(line)
                all_lines_set.add(l_strip)
    with open(fn, "w") as f_out:
        f_out.writelines(sorted(all_lines))
