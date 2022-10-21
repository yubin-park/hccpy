import unittest
import numpy as np
from hccpy.hcc import HCCEngine


class TestHCCEngine(unittest.TestCase):

    def test_esrd(self):
        he = HCCEngine("ESRDv21")
        rp = he.profile(["E0952"])
        self.assertTrue("HCC18" in rp["hcc_map"]["E0952"])
        self.assertTrue("HCC106" in rp["hcc_map"]["E0952"])
        self.assertTrue("HCC108" in rp["hcc_map"]["E0952"])

        rp = he.profile(["E083599"])
        self.assertTrue("HCC18" in rp["hcc_map"]["E083599"])
        self.assertTrue("HCC122" in rp["hcc_map"]["E083599"])


if __name__ == "__main__":

    unittest.main()


