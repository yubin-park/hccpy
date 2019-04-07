import numpy as np
import csv
import json
from pkg_resources import resource_filename
from collections import Counter
import hccpy.utils as utils
import hccpy.V22I0ED2 as V22I0ED2
import hccpy.V2218O1M as V2218O1M
import hccpy.V2318P1M as V2318P1M

class HCCEngine:

    def __init__(self, version = "22"):
       
        dx2ccfn = resource_filename(__name__, "data/F2218O1P.TXT")
        coeffn = resource_filename(__name__, "data/V22hcccoefn.csv")
        labelfn = resource_filename(__name__, "data/V22H79L1.TXT")
        hierfn = resource_filename(__name__, "data/V22H79H1.TXT")
        if version == "23":
            dx2ccfn = resource_filename(__name__, "data/F2318P1Q.TXT")
            coeffn = resource_filename(__name__, "data/V23hcccoefn.csv")
            labelfn = resource_filename(__name__, "data/V23H83L2.TXT")
            hierfn = resource_filename(__name__, "data/V23H83H1.TXT")

        self.version = version
        self.dx2cc = utils.read_dx2cc(dx2ccfn)
        self.coefn = utils.read_coefn(coeffn)
        self.label = utils.read_label(labelfn)
        self.hier = utils.read_hier(hierfn)

    def _apply_hierarchy(self, cc_lst):

        cc_cnt = Counter(cc_lst)
        for k, v in self.hier.items():
            if k in cc_cnt:
                for v_i in v:
                    cc_cnt[v_i] -= 1
        cc_lst = [k for k, v in cc_cnt.items() if v > 0]

        return cc_lst

    def apply_hcc(self, dx_lst, age=-1, sex="U", disabled=0):

        dx_set = {dx.strip().upper().replace(".","") for dx in dx_lst}
        cc_dct = {dx:self.dx2cc[dx] for dx in dx_set if dx in self.dx2cc}

        cc_lst = V22I0ED2.apply_agesex_edits(cc_dct, age, sex)
        cc_lst = self._apply_hierarchy(cc_lst)
        if self.version == "22":
            cc_lst = V2218O1M.create_interactions(cc_lst, disabled)
        elif self.version == "23":
            cc_lst = V2318P1M.create_interactions(cc_lst, disabled, age)

        return cc_lst

    def calculate_risk(self, hcc_lst, age=70, sex="M", 
                        elig="CNA", origds=0):
        risk_dct = {}
    
        # demographic factors
        elig_demo = elig + "_" + sex
        age_ranges = [x for x in self.coefn if elig_demo in x]
        age_match = age_ranges[0]
        for age_range in age_ranges:
            age_tokens = age_range.replace(elig_demo, "").split("_") 
            lb, ub = 0, 999 
            if len(age_tokens) == 1:
                lb = int(age_tokens[0])
                ub = lb + 1
            elif age_tokens[1] == "GT":
                lb = int(age_tokens[0])
            else: 
                lb = int(age_tokens[0])
                ub = int(age_tokens[1]) + 1
            if lb <= age < ub:
                age_match = age_range
                break
        risk_dct[age_match] = self.coefn[age_match]

        if origds > 0:
            elig_origds = elig + "_OriginallyDisabled_"
            if sex == "M":
                elig_origds += "Male" 
            else:
                elig_origds += "Femle" 
            if elig_origds in self.coefn:
                risk_dct[elig_origds] = self.coefn[elig_origds]

        # hcc factors
        for hcc in hcc_lst:
            elig_hcc = elig + "_" + hcc
            if elig_hcc in self.coefn:
                risk_dct[elig_hcc] = self.coefn[elig_hcc]

        return risk_dct

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

        disabled = 0
        if age < 65 and orec != "0":
            disabled = 1
        origds = 0
        if orec == "1" and disabled == 0:
            origds = 1
        if elig in {"NE", "SNPNE"}:
            edit = ""
            if medicaid:
                elig += "_MCAID"
            else:
                elig += "_NMCAID"
            if origds > 0:
                elig += "_ORIGDIS_NE"
            else:
                elig += "_NORIGDIS_NE"

        hcc_lst = self.apply_hcc(dx_lst, age, sex, disabled)
        risk_dct = self.calculate_risk(hcc_lst, age, sex, elig, origds)

        raf = np.sum([x for x in risk_dct.values()])
        out = {
                "risk_score": raf,
                "details": risk_dct,
                "parameters": {
                    "age": age,
                    "sex": sex,
                    "elig": elig,
                    "medicaid": medicaid,
                    "disabled": disabled,
                    "origds": origds
                    }
                }
        return out


