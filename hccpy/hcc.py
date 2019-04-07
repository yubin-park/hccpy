import numpy as np
from collections import Counter
import hccpy.utils as utils
import hccpy._V22I0ED2 as V22I0ED2 # age sex edits (v22, v23)
import hccpy._V2218O1M as V2218O1M # interactions (v22)
import hccpy._V2318P1M as V2318P1M # interactions (v23)
import hccpy._AGESEXV2 as AGESEXV2 # disabled/origds (v22, v23)
import hccpy._V2218O1P as V2218O1P # risk coefn (v22, v23)

class HCCEngine:

    def __init__(self, version="22"):
        fnmaps = {
                    "22": {
                            "dx2cc": "data/F2218O1P.TXT",
                            "coefn": "data/V22hcccoefn.csv",
                            "label": "data/V22H79L1.TXT",
                            "hier": "data/V22H79H1.TXT"
                    },
                    "23": {
                            "dx2cc": "data/F2318P1Q.TXT",
                            "coefn": "data/V23hcccoefn.csv",
                            "label": "data/V23H83L2.TXT",
                            "hier": "data/V23H83H1.TXT"
                    }
                }
        self.version = version
        self.dx2cc = utils.read_dx2cc(fnmaps[version]["dx2cc"])
        self.coefn = utils.read_coefn(fnmaps[version]["coefn"])
        self.label = utils.read_label(fnmaps[version]["label"])
        self.hier = utils.read_hier(fnmaps[version]["hier"])

    def _apply_hierarchy(self, cc_lst):

        cc_cnt = Counter(cc_lst)
        for k, v in self.hier.items():
            if k in cc_cnt:
                for v_i in v:
                    cc_cnt[v_i] -= 1
        cc_lst = [k for k, v in cc_cnt.items() if v > 0]

        return cc_lst

    def _apply_hcc(self, dx_lst, age, sex, disabled):
        """Returns all HCC variables regardless of the eligibility segments.
        """

        dx_set = {dx.strip().upper().replace(".","") for dx in dx_lst}
        cc_dct = {dx:self.dx2cc[dx] for dx in dx_set if dx in self.dx2cc}

        cc_lst = V22I0ED2.apply_agesex_edits(cc_dct, age, sex)
        cc_lst = self._apply_hierarchy(cc_lst)
        if self.version == "22":
            cc_lst = V2218O1M.create_interactions(cc_lst, disabled)
        elif self.version == "23":
            cc_lst = V2318P1M.create_interactions(cc_lst, disabled, age)

        return cc_lst

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

        disabled, origds, elig = AGESEXV2.get_ds(age, orec, medicaid, elig)
        hcc_lst = self._apply_hcc(dx_lst, age, sex, disabled)
        risk_dct = V2218O1P.get_risk_dct(self.coefn, hcc_lst, age, 
                                        sex, elig, origds)

        score = np.sum([x for x in risk_dct.values()])
        out = {
                "risk_score": score,
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


