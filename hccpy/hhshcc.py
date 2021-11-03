import numpy as np
from collections import Counter
import hccpy.utils_hhs as utils
import hccpy._AGESEXV6 as AGESEXV6 # age/sex variables
import hccpy._I0V05ED2 as I0V05ED2 # age/sex edits
import hccpy._V0519F3M as V0519F3M # interactions
import hccpy._V0519F3P as V0519F3P # risk coefn 

class HHSHCCEngine:

    def __init__(self, myear="2019"):
        
        fnmaps = {
                "2019": {
                    "dx2cc": "data/H0519F3.FY 2019 ICD10.TXT",
                    "ndc2rxc": "data/H0519F3_NDC.4_4.1812.TXT",
                    "hcpcs2rxc": "data/H0519F3_HCPCS.4_4.1812.TXT",
                    "coefn": "data/HHS19hcccoefn.csv",
                    "label": "data/V05128L1.TXT",
                    "hier": "data/V05128H1.TXT"
                }
            }
        self.myear = myear
        self.dx2cc = utils.read_dx2cc(fnmaps[myear]["dx2cc"])
        self.ndc2rxc = utils.read_code2rxc(fnmaps[myear]["ndc2rxc"])
        self.hcpcs2rxc = utils.read_code2rxc(fnmaps[myear]["hcpcs2rxc"])
        self.coefn = utils.read_coefn(fnmaps[myear]["coefn"])
        self.label = utils.read_label(fnmaps[myear]["label"])
        self.hier = utils.read_hier(fnmaps[myear]["hier"])

    def _apply_hierarchy(self, cc_dct, age, sex):
        """Returns a list of HCCs after applying hierarchy and age/sex edit
        """
        cc_cnt = Counter(set(cc_dct.values()))
        for k, v in self.hier.items():
            if k in cc_cnt:
                for v_i in v:
                    cc_cnt[v_i] -= 1
        cc_lst = [k for k, v in cc_cnt.items() if v > 0]
        return cc_lst

    def _apply_interactions(self, cc_lst, agegroup, age):
        """Returns a list of HCCs after applying interactions.
        """
        cc_lst = V0519F3M.create_interactions(cc_lst, agegroup, age)
        return cc_lst

    def _sexmap(self, sex):
        smap = {"0": "F", # originally, Unknown
                "1": "M",
                "2": "F",
                "male": "M",
                "female": "F",
                "unknown": "F"}
        if sex.lower() in smap:
            sex = smap[sex.lower()]
        return sex

    def profile(self, dx_lst, pr_lst=[], rx_lst=[], 
                age=20, sex="M", enroll_months=10, plate="S"):
        """Returns the HCC risk profile of a given patient information.

        Parameters
        ----------
        dx_lst : list of str
                 A list of ICD10 codes for the measurement year.
        pr_lst : list of str
                 A list of HCPCS codes for the measurement year.
        rx_lst : list of str
                 A list of NDC codes for the measurement year.
        age : int or float
              The age of the patient.
        sex : str 
              The sex of the patient; {"M", "F"}
        enroll_months : int
              The number of months the patient was enrolled
        """

        sex = self._sexmap(sex)
        agesexvar, agegroup = AGESEXV6.get_agesex(age, sex)
        enroll_months = str(enroll_months)
        enroll_dur = "ED_"+enroll_months

        # dx2cc
        dx_set = {dx.strip().upper().replace(".","") for dx in dx_lst}
        cc_dct = {dx:self.dx2cc[dx] for dx in dx_set if dx in self.dx2cc}
        
        # rxc
        cc_dct.update({ndc:self.ndc2rxc[ndc] for ndc in rx_lst
                        if ndc in self.ndc2rxc})
        cc_dct.update({hcpcs:self.hcpcs2rxc[pr] for pr in pr_lst
                        if pr in self.hcpcs2rxc})

        cc_dct = I0V05ED2.apply_agesex_edits(cc_dct, age, sex)
        hcc_lst_0 = self._apply_hierarchy(cc_dct, age, sex)
        hcc_lst = self._apply_interactions(hcc_lst_0, agegroup, age)
        risk_dct = V0519F3P.get_risk_dct(self.coefn, hcc_lst, 
                                            agesexvar, agegroup, enroll_dur, plate) 

        score = np.sum([x for x in risk_dct.values()])
        out = {
                "risk_score": score,
                "details": risk_dct,
                "hcc_lst": hcc_lst_0,   # HCC list before interactions
                "hcc_map": cc_dct,     # before applying hierarchy
                "parameters": {
                    "age": age,
                    "sex": sex,
                    "enroll_months": enroll_months
                    }
                }
        return out

    def diff(self, before=[], after=[]):
        """
        Return the difference between two HCC lists (before and after)
       
        Background
        ----------
        CCs evolve over years. As patients get older, new CCs are added, 
        some pre-exisited CCs may disappear. Sometimes, CCs get assigned to
        a higher level (or parent) CCs as the conditinos become more 
        serious. This module provides the difference between "before" and
        "after" and highlights what are "added (both new and upgraded)", 
        "deleted".

        Parameters
        ----------
        before : list
                a list of CCs that were present before
        after : list
                a list of CCs that are present curretly
        """
        before_set = set(before)
        after_set = set(after)
        added_set = after_set - before_set
        deleted_set = before_set - after_set

        for added_item in added_set:
            if added_item not in self.hier:
                continue
            for child_item in self.hier[added_item]:
                if child_item in deleted_set:
                    deleted_set.remove(child_item)

        out = {
            "added": list(added_set),
            "deleted": list(deleted_set)
            }

        return out




