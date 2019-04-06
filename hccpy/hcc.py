import numpy as np
import csv
import json
from pkg_resources import resource_filename
from collections import Counter
import hccpy.utils as utils

class HCCEngine:

    def __init__(self, 
                dx2ccfn="F2218O1P.TXT",
                coeffn="V22hcccoefn.csv",
                labelfn="V22H79L1.TXT",
                hierfn="V22H79H1.TXT"):
        dx2ccpath = resource_filename(__name__, "data/" + dx2ccfn)
        coefpath = resource_filename(__name__, "data/" + coeffn)
        labelpath = resource_filename(__name__, "data/" + labelfn)
        hierpath = resource_filename(__name__, "data/" + hierfn)
        self.dx2cc = utils.read_dx2cc(dx2ccpath)
        self.coef = utils.read_coef(coefpath)
        self.label = utils.read_label(labelpath)
        self.hier = utils.read_hier(hierpath)

    def _apply_hierarchy(self, cc_lst):
        cc_cnt = Counter(cc_lst)
        for k, v in self.hier.items():
            if k in cc_cnt:
                for v_i in v:
                    cc_cnt[v_i] -= 1
        cc_lst = [k for k, v in cc_cnt.items() if v > 0]
        return cc_lst

    def _create_interactions(self, cc_lst):

        

        return cc_lst

    def _get_cc(self, dx_lst, age=-1, sex="U"):
        dx_set = {dx.strip().upper().replace(".","") for dx in dx_lst}
        cc_dct = {dx:self.dx2cc[dx] for dx in dx_set if dx in self.dx2cc}

        # age/sex edits. see "V22I0ED2.TXT"
        elst0 = ["D66", "D67"]
        elst1 = ["J410", "J411", "J418", "J42", "J430", "J431", "J432", 
                "J438", "J439", "J440", "J441", "J449", "J982", "J983"]
        elst2 = ["F3481"]
        if sex == "2":
            for dx in (dx for dx in elst0 if dx in cc_dct):
                cc_dct[dx] = "48" 
        elif age > -1 and age < 18:
            for dx in (dx for dx in elst1 if dx in cc_dct):
                cc_dct[dx] = "112"
        elif age > -1 and (age < 6 or age > 18):
            for dx in (dx for dx in elst2 if dx in cc_dct):
                cc_dct[dx] = "-1"
        cc_lst = [cc for cc in cc_dct.values() if cc != "-1"]

        cc_lst = self._apply_hierarchy(cc_lst)
        cc_lst = self._create_interactions(cc_lst)       
 
        return cc_lst

    def _get_risk(self, cc_lst, eligibility=""):
        risk_score = 0.0

        return risk_score

    def profile(self, dx_lst, age=-1, sex="U", eligibility=""):

        cc_lst = self._get_cc(dx_lst, age, sex)
        risk_score = _get_risk(cc_lst, eligibility)





