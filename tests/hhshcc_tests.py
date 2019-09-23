import unittest
import numpy as np
from hccpy.hhshcc import HHSHCCEngine


class TestHHSHCCEngine(unittest.TestCase):

    def test_hccmapping(self):

        hhe = HHSHCCEngine()
        rp = hhe.profile(["E1169"])
        self.assertTrue("G01" in rp["details"])
        self.assertTrue("HHS_HCC020" in rp["hcc_map"].values())

        rp = hhe.profile(["P0411"], age=1)
        self.assertTrue("AGE1_X_SEVERITY2" in rp["details"])

        rp = hhe.profile(["P0411"], age=10)
        self.assertTrue(len(rp["hcc_lst"])==0)

        rp = hhe.profile(["E1169", "I5030", "I509", "I211", "I209", "R05"])
        self.assertTrue("HHS_HCC130" in rp["details"])

if __name__ == "__main__":

    unittest.main()


