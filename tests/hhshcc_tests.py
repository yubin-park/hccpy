import unittest
import numpy as np
from hccpy.hhshcc import HHSHCCEngine


class TestHHSHCCEngine(unittest.TestCase):

    def test_hccmapping_y19(self):

        hhe = HHSHCCEngine(myear="2019")
        rp = hhe.profile(["E1169"])
        self.assertTrue("G01" in rp["details"])
        self.assertTrue("HHS_HCC020" in rp["hcc_map"].values())

        rp = hhe.profile(["P0411"], age=1)
        self.assertTrue("AGE1_X_SEVERITY2" in rp["details"])

        rp = hhe.profile(["P0411"], age=10)
        self.assertTrue(len(rp["hcc_lst"])==0)

        rp = hhe.profile(["E1169", "I5030", "I509", "I211", "I209", "R05"])
        self.assertTrue("HHS_HCC130" in rp["details"])

        rp = hhe.profile([], rx_lst=["00003196401"], age=45)
        self.assertTrue("RXC_01" in rp["details"])


    def test_hccmapping_y22(self):

        hhe = HHSHCCEngine(myear="2022")
        rp = hhe.profile(["E1169"])
        self.assertTrue("G01" in rp["details"])
        self.assertTrue("HHS_HCC020" in rp["hcc_map"].values())

        rp = hhe.profile(["P0411"], age=1)
        self.assertTrue("AGE1_X_SEVERITY2" in rp["details"])

        rp = hhe.profile(["P0411"], age=10)
        self.assertTrue(len(rp["hcc_lst"])==0)

        rp = hhe.profile(["E1169", "I5030", "I509", "I211", "I209", "R05"])
        self.assertTrue("HHS_HCC130" in rp["details"])

        rp = hhe.profile([], rx_lst=["00003196401"], age=45)
        self.assertTrue("RXC_01" in rp["details"])

if __name__ == "__main__":

    unittest.main()


