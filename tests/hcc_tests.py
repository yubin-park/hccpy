import unittest
import numpy as np
from hccpy.hcc import HCCEngine


class TestHCCEngine(unittest.TestCase):

    def test_hccmapping(self):

        he = HCCEngine()
        rp = he.profile(["E1169"], elig="CNA")
        self.assertTrue("CNA_HCC18" in rp["details"])

        rp = he.profile(["I209"], elig="CNA")
        self.assertTrue("CNA_HCC88" in rp["details"])


    def test_demomapping(self):

        he = HCCEngine()
        rp = he.profile([], age=70, sex="M", elig="CNA")
        self.assertTrue("CNA_M70_74" in rp["details"])

        rp = he.profile([], age=23, sex="F", elig="CPD")
        self.assertTrue("CPD_F0_34" in rp["details"])

        rp = he.profile([], age=67, sex="M", elig="CNA", orec="1")
        self.assertTrue("CNA_M65_69" in rp["details"])
        self.assertTrue("CNA_OriginallyDisabled_Male" in rp["details"])

        rp = he.profile([], age=66, sex="M", elig="NE")
        self.assertTrue("NE_NMCAID_NORIGDIS_NEM66" in rp["details"])

        rp = he.profile([], age=66, sex="M", elig="SNPNE", medicaid=True)
        self.assertTrue("SNPNE_MCAID_NORIGDIS_NEM66" in rp["details"])


    def test_riskscore(self):

        he = HCCEngine()

        rp = he.profile(["E1169", "I509"], age=70, sex="M", elig="CNA")
        self.assertTrue(np.isclose(rp["risk_score"], 1.174))

        rp = he.profile(["E1169", "I5030", "I509", "I211", "I209", "R05"],
                        age=70, sex="M", elig="CNA")
        self.assertTrue(np.isclose(rp["risk_score"], 1.314))

        rp = he.profile(["E1169", "I5030", "I509", "I211", "I209", "R05"],
                        age=45, sex="F", elig="CND")
        self.assertTrue(np.isclose(rp["risk_score"], 1.322))


    def test_version(self):

        he = HCCEngine(version="22")
        rp = he.profile(["E1169", "I5030", "I509", "I211", "I209", "R05"],
                        age=70, sex="M", elig="CNA")
        self.assertTrue(np.isclose(rp["risk_score"], 1.314))

        he = HCCEngine(version="23")
        rp = he.profile(["E1169", "I5030", "I509", "I211", "I209", "R05"],
                        age=70, sex="M", elig="CNA")
        self.assertTrue(np.isclose(rp["risk_score"], 1.3))


    def test_hccdescription(self):

        he = HCCEngine()

        doc = he.describe_hcc("19")
        self.assertTrue(doc["description"] == "Diabetes without Complication")

        doc = he.describe_hcc("HCC19")
        self.assertTrue(doc["description"] == "Diabetes without Complication")

        doc = he.describe_hcc("hcc19")
        self.assertTrue(doc["description"] == "Diabetes without Complication")

        doc = he.describe_hcc("3")
        self.assertTrue(doc["description"] == "N/A")


    def test_hccfamily(self):

        he = HCCEngine()

        doc = he.describe_hcc("19")
        self.assertTrue("HCC17" in doc["parents"])
        self.assertTrue("HCC18" in doc["parents"])

        doc = he.describe_hcc("HCC19")
        self.assertTrue("HCC17" in doc["parents"])
        self.assertTrue("HCC18" in doc["parents"])

        doc = he.describe_hcc("HCC19")
        self.assertTrue(len(doc["children"]) == 0)

        doc = he.describe_hcc("17")
        self.assertTrue("HCC18" in doc["children"])
        self.assertTrue("HCC19" in doc["children"])

    def test_diff(self):

        he = HCCEngine()
        out = he.diff(before=["HCC18"], after=["HCC18", "HCC01"])
        self.assertTrue("HCC01" in out["added"])

        out = he.diff(before=["HCC19"], after=["HCC18", "HCC01"])
        self.assertTrue("HCC01" in out["added"])
        self.assertTrue("HCC19" not in out["deleted"])
        self.assertEqual(len(out["deleted"]), 0)

if __name__ == "__main__":

    unittest.main()


