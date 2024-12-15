import numpy as np
import re
from collections import Counter
import hccpy.utils as utils
import hccpy._V22I0ED2 as V22I0ED2 # age sex edits (v22, v23, v24)
import hccpy._V28I0ED1 as V28I0ED1 # age sex edits (v28)
import hccpy._V2218O1M as V2218O1M # interactions (v22)
import hccpy._V2318P1M as V2318P1M # interactions (v23)
import hccpy._V2419P1M as V2419P1M # interactions (v24)
import hccpy._V2823T2M as V2823T2M # interactions (v28)
import hccpy._E2118P1M as E2118P1M # interactions (ESRD)
import hccpy._AGESEXV2 as AGESEXV2 # disabled/origds (v22, v23, v24, v28)
import hccpy._V2218O1P as V2218O1P # risk coefn (v22, v23, v24, v28)
import hccpy._E2118P1P as E2118P1P # risk coefn for ESRD


class HCCEngine:

    def __init__(self, 
                version="24", 
                dx2cc_year="Combined", 
                cif = 0.059, # coding intensity factor. 
                norm_params={ # please see the note below. 
                    "C": 1.015, 
                    "D": 1.022, 
                    "G": 1.028
                    }
                ):
        # NOTE: contributed/inspired by @ronnie-canopy
        #       modified by @yubin-park, for backward compatibility and 
        #           extensibility
        # Normalization Params (norm_params) can be configured manuallly
        # By default, it has the 2024 normalization factors for now
        # norm_parms need to have three keys, C, D, and G. 
        #   C is for the community and institutional models, and
        #   D and G for ESRD models; dialsys and functional graft.
        # norm_params can change every year. For example,
        # V24, Y2022, {"C": 1.118}
        #       Y2023, {"C": 1.127}
        #       Y2024, {"C": 1.146}
        # V28, Y2024, {"C": 1.015}
        # ESRDv21, Y2022, {"D": 1.077, "G": 1.126}
        #           Y2023, {"D": 1.034, "G": 1.048}
        #           Y2024, {"D": 1.022,  "G": 1.028}

        fnmaps = {
            "22": {
                "dx2cc": {"2017": "data/F2217O1P.TXT",
                          "2018": "data/F2218O1P.TXT",
                          "2019": "data/F2219O1P.TXT",
                          "2020": "data/F2220O1P.TXT",
                          "2021": "data/F2221O1P.TXT",
                          "2022": "data/F2222O1P.TXT",  # finalized mappings
                          "Combined": "data/F22_AllYearsCombined.TXT"},
                "coefn": "data/V22hcccoefn.csv",
                "label": "data/V22H79L1.TXT",
                "hier": "data/V22H79H1.TXT"
            },
            "23": {
                "dx2cc": {"2018": "data/F2318P1Q.TXT",
                          "2019": "data/F2319P1Q.TXT",
                          "Combined": "data/F23_AllYearsCombined.TXT"},  # CMS has not provided updated mappings
                "coefn": "data/V23hcccoefn.csv",
                "label": "data/V23H83L2.TXT",
                "hier": "data/V23H83H1.TXT"
            },
            "24": {
                "dx2cc": {"2019": "data/F2419P1M.TXT",
                          "2020": "data/F2420P1M.TXT",
                          "2021": "data/F2421P1M.TXT",
                          "2022": "data/F2422P1M.TXT",  # finalized mappings
                          "Combined": "data/F24_AllYearsCombined.TXT"},
                "coefn": "data/V24hcccoefn.csv",
                "label": "data/V24H86L1.TXT",
                "label_short": "data/V24_label_short.json",
                "hier": "data/V24H86H1.TXT"
            },
            "28": {
                "dx2cc": {"2024": "data/F2824T1N.TXT", 
                          "Combined": "data/F2824T1N.TXT"},
                "coefn": "data/V28hcccoefn.csv",
                "label": "data/V28115L3.TXT",
                "hier": "data/V28115H1.TXT"
            },
            "ESRDv21": {
                "dx2cc": {"2019": "data/F2118H1R.txt",
                          "Combined": "data/F2118H1R.txt"},
                "coefn": "data/ESRDhcccoefn.csv",
                "label": "data/V20H87L1.txt",
                "hier": "data/V20H87H1.txt"
            }
        }

        assert fnmaps[version]["dx2cc"].get(dx2cc_year), "Invalid combination of version and year parameters"
        self.version = version
        self.cif = cif
        self.norm_params = norm_params
        self.dx2cc = utils.read_dx2cc(fnmaps[version]["dx2cc"][dx2cc_year])
        self.coefn = utils.read_coefn(fnmaps[version]["coefn"])
        self.label = utils.read_label(fnmaps[version]["label"])
        self.hier = utils.read_hier(fnmaps[version]["hier"])
        self.label_short = {}
        if "label_short" in fnmaps[version]:
            self.label_short = utils.read_label_short(
                                fnmaps[version]["label_short"])

    def _apply_hierarchy(self, cc_dct, age, sex):
        """Returns a list of HCCs after applying hierarchy and age/sex edit
        """
        cc_lst_all = []
        for dx, cc_lst in cc_dct.items():
            cc_lst_all += [cc for cc in cc_lst if cc != "HCCNA"]
        cc_cnt = Counter(set(cc_lst_all))
         
        if self.version == "28": # V28 weird patch for heart
            if (cc_cnt["HCC223"] > 0 and 
                (cc_cnt["HCC221"] + cc_cnt["HCC222"] + 
                cc_cnt["HCC224"] + cc_cnt["HCC225"] + 
                cc_cnt["HCC226"]) == 0):
                cc_cnt["HCC223"] = 0
        
        for k, v in self.hier.items():
            if k in cc_cnt:
                for v_i in v:
                    cc_cnt[v_i] -= 1

        cc_lst_unique = [k for k, v in cc_cnt.items() if v > 0]
        return cc_lst_unique

    def _apply_interactions(self, cc_lst, age, disabled):
        """Returns a list of HCCs after applying interactions.
        """
        if self.version == "22":
            cc_lst = V2218O1M.create_interactions(cc_lst, disabled)
        elif self.version == "23":
            cc_lst = V2318P1M.create_interactions(cc_lst, disabled, age)
        elif self.version == "24":
            cc_lst = V2419P1M.create_interactions(cc_lst, disabled, age)
        elif self.version == "28":
            cc_lst = V2823T2M.create_interactions(cc_lst, disabled, age)
        elif self.version == "ESRDv21":
            cc_lst = E2118P1M.create_interactions(cc_lst, disabled, age)

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

    def profile(self, dx_lst, age=70, sex="M", 
                    elig="CNA", orec="0", medicaid=False):
        """Returns the HCC risk profile of a given patient information.

        Parameters
        ----------
        dx_lst : list of str
                 A list of ICD10 codes for the measurement year.
        age : int or float
              The age of the patient.
        sex : str 
              The sex of the patient; {"M", "F"}
        elig : str
               The eligibility segment of the patient.
               Allowed values are as follows:
               - "CFA": Community Full Benefit Dual Aged
               - "CFD": Community Full Benefit Dual Disabled
               - "CNA": Community NonDual Aged
               - "CND": Community NonDual Disabled
               - "CPA": Community Partial Benefit Dual Aged
               - "CPD": Community Partial Benefit Dual Disabled
               - "INS": Long Term Institutional
               - "NE": New Enrollee
               - "SNPNE": SNP NE
        orec: str
              Original reason for entitlement code.
              - "0": Old age and survivor's insurance
              - "1": Disability insurance benefits
              - "2": End-stage renal disease 
              - "3": Both DIB and ESRD
        medicaid: bool
                  If the patient is in Medicaid or not.
        """

        sex = self._sexmap(sex)
        disabled, origds, elig = AGESEXV2.get_ds(age, orec, medicaid, elig)

        dx_set = {dx.strip().upper().replace(".","") for dx in dx_lst}
        cc_dct = {dx:self.dx2cc[dx] for dx in dx_set if dx in self.dx2cc}
        if self.version == "28": 
            cc_dct = V28I0ED1.apply_agesex_edits(cc_dct, age, sex) 
        else: 
            cc_dct = V22I0ED2.apply_agesex_edits(cc_dct, age, sex) 
        hcc_lst = self._apply_hierarchy(cc_dct, age, sex)
        hcc_lst = self._apply_interactions(hcc_lst, age, disabled)
        if "ESRD" not in self.version:
            risk_dct = V2218O1P.get_risk_dct(self.coefn, hcc_lst, age, 
                                        sex, elig, origds, medicaid)
        else:
            risk_dct = E2118P1P.get_risk_dct(self.coefn, hcc_lst, age, sex)

        score = round(np.sum([x for x in risk_dct.values()]), 4)

        demo_pttrn = r'[MF]\d{1,2}_?|[MF]6[5-9]|OriginallyDisabled_[MF]|LTIMCAID|ORIGDS'
        score_age = round(np.sum([v for k, v in risk_dct.items() 
                            if re.search(demo_pttrn, k)]), 4)

        # by @ronnie-canopy
        # apply normalization and 
        # coding pattern adjustment when computing pricing RAF
        adj_factor = 1
        nf = 1 # normalization factor
        if "ESRD" in self.version:
            # We assume elig for ESRD is one of 
            #   "DI", "GC", "GI", "DNE", "GNE"
            nf = self.norm_params[elig[0]]
        else:
            nf = self.norm_params["C"]

        adj_factor = (1 - self.cif) / nf
        score_adj = round(score * adj_factor, 4)
        score_age_adj = round(score_age * adj_factor, 4)

        out = {
                "risk_score": score,
                "risk_score_age": score_age,
                "risk_score_adj": score_adj,
                "risk_score_age_adj": score_age_adj,
                "details": risk_dct,
                "hcc_lst": hcc_lst,    # HCC list before interactions
                "hcc_map": cc_dct,     # before applying hierarchy
                "parameters": {
                    "age": age,
                    "sex": sex,
                    "elig": elig,
                    "medicaid": medicaid,
                    "disabled": disabled,
                    "origds": origds
                    },
                "model": self.version
                }
        return out

    def describe_hcc(self, cc):
        """
        Return the medical description of a given Condition Category
        
        Parameters
        ----------
        cc : str
            The Condition Category of interest
        """
        cc = cc.upper()
        # cc needs no prefix "HCC"
        cc_desc = self.label.get(cc.replace("HCC", ""), "N/A")  
        cc_desc_short = self.label_short.get(cc.replace("HCC", ""), "N/A")  
        if "HCC" not in cc:
            cc = "HCC{}".format(cc)
        cc_children = self.hier.get(cc, [])
        cc_parents = []
        for k, v in self.hier.items():
            if cc in v:
                cc_parents.append(k)
        out = {
            "description": cc_desc,
            "desc_short": cc_desc_short,
            "children": cc_children,
            "parents": cc_parents
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




