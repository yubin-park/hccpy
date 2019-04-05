import numpy as np
import csv
import json
from pkg_resources import resource_filename

class HCCEngine:

    def __init__(self, modelyear=2019, version="22"):
        self.modelyear = modelyear
        self.version = version
        self.dx2cc = {}
        self.coef = {}
        dx2cc_fn = resource_filename(__name__, "data/F2218O1P.TXT")
        with open(dx2cc_fn, "r") as fp:
            reader = csv.reader(fp, delimiter="\t")
            self.dx2cc = {row[0]:row[1] for row in reader}
        coef_fn = resource_filename(__name__, "data/hcccoefn.csv")
        with open(coef_fn, "r") as fp:
            reader = csv.reader(fp, delimiter=",")
            header = next(reader)
            values = [float(x) for x in next(reader)]
            self.coef = {k: v for k, v in zip(header, values)}

    def _get_hcc(self, dx_lst):

        pass

    def _get_risk(self, hcc_lst, eligibility=""):

        pass

     




