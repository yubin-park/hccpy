import unittest
import numpy as np
from hccpy.raeligible import RAEligible


class TestRAEligible(unittest.TestCase):

    def test_raeligible(self):
       
        rae = RAEligible()

        # NOTE: you need to place the file in the same test folder
        rae.load(fn="CY2019Q2_CPTHCPCS_CMS_20190425.csv") 
        
        out = rae.is_eligible(pr_lst=["C5271"])
        self.assertEqual(out, True)

        out = rae.is_eligible(pr_lst=["C5270"])
        self.assertEqual(out, False)

        out = rae.is_eligible(pr_lst=["C5270"], claimtype="outpatient")
        self.assertEqual(out, False)

        out = rae.is_eligible(pr_lst=["C5270"], billtype="121",
                            claimtype="outpatient")
        self.assertEqual(out, False)

        out = rae.is_eligible(pr_lst=["C5271"], billtype="121",
                            claimtype="outpatient")
        self.assertEqual(out, True)

        out = rae.is_eligible(billtype="121", claimtype="inpatient")
        self.assertEqual(out, False)

        out = rae.is_eligible(billtype="111", claimtype="inpatient")
        self.assertEqual(out, True)





if __name__ == "__main__":

    unittest.main()


