## Hierachical Condition Categories Python Package (hccpy)

This module implements the Hierachical Condition Categories that are used for adjusting risks for the Medicare population.

## Installing

Installing from the source:

```
$ git clone git@github.com:yubin-park/hccpy
$ cd hccpy
$ python setup.py develop
```
Or, simply using `pip`:

```
$ pip install hccpy
```

## Code Examples

`hccpy` is really simple to use.
Please see some examples below:

```python
>>> import json
>>> from hccpy.hcc import HCCEngine
>>> he = HCCEngine()
>>> print(he.profile.__doc__)
Returns the HCC risk profile of a given patient information.

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
>>>
>>> rp = he.profile(["E1169", "I5030", "I509", "I211", "I209", "R05"])
>>> print(json.dumps(rp, indent=2))
{
  "risk_score": 1.314,
  "details": {
    "CNA_M70_74": 0.379,
    "CNA_HCC18": 0.318,
    "CNA_HCC85": 0.323,
    "CNA_HCC88": 0.14,
    "CNA_HCC85_gDiabetesMellit": 0.154
  },
  "parameters": {
    "age": 70,
    "sex": "M",
    "elig": "CNA",
    "medicaid": false,
    "disabled": 0,
    "origds": 0
  }
}
>>>
>>> rp = he.profile([], elig="NE", age=65)
>>> print(json.dumps(rp, indent=2))
{
  "risk_score": 0.514,
  "details": {
    "NE_NMCAID_NORIGDIS_NEM65": 0.514
  },
  "parameters": {
    "age": 65,
    "sex": "M",
    "elig": "NE_NMCAID_NORIGDIS_NE",
    "medicaid": false,
    "disabled": 0,
    "origds": 0
  }
}
>>>
>>> rp = he.profile(["E1169", "I5030", "I509", "I209"], elig="INS")
>>> print(json.dumps(rp, indent=2))
{
  "risk_score": 2.6059999999999994,
  "details": {
    "INS_M70_74": 1.323,
    "INS_HCC88": 0.497,
    "INS_HCC85": 0.191,
    "INS_HCC18": 0.441,
    "INS_DIABETES_CHF": 0.154
  },
  "parameters": {
    "age": 70,
    "sex": "M",
    "elig": "INS",
    "medicaid": false,
    "disabled": 0,
    "origds": 0
  }
}
```

## Authors
- Yubin Park, PhD

## References
- https://www.nber.org/data/cms-risk-adjustment.html
- https://www.cms.gov/medicare/health-plans/medicareadvtgspecratestats/risk-adjustors.html
- https://github.com/calyxhealth/pyriskadjust
- https://github.com/AlgorexHealth/hcc-python
- https://github.com/galtay/hcc_risk_models



