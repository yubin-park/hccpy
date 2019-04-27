# hccpy 

Hierachical Condition Categories Python Package.

This module implements the [Hierachical Condition Categories](https://www.cms.gov/cciio/resources/forms-reports-and-other-resources/downloads/ra-march-31-white-paper-032416.pdf) that are used for adjusting risks for the Medicare population.
The original SAS implementation can be found [here](https://www.nber.org/data/cms-risk-adjustment.html).

NOTE that this package does not support for ICD-9.

## Installing

Installing from the source:

```
$ git clone git@github.com:yubin-park/hccpy.git
$ cd hccpy
$ python setup.py develop
```
Or, simply using `pip`:

```
$ pip install hccpy
```

## File Structure

- `hccpy/ `: The package source code is located here.
  - `data/`: The raw data files directly downloaded from [the National Burequ of Economics Research](https://www.nber.org/data/cms-risk-adjustment.html)
    - Here, you see the original SAS scripts and data files for the CMS HCC models.
  - `_AGESEXV2.py`: a Python re-write of the `AGESEXV2.TXT` SAS script.
  - `_V2218O1M.py`: a Python re-write of the `V2218O1M.TXT` SAS script.
  - `_V2218O1P.py`: a Python re-write of the `V2219O1P.TXT` SAS script.
  - `_V22I0ED2.py`: a Python re-write of the `V22I0ED2.TXT` SAS script.
  - `_V2318P1M.py`: a Python re-write of the `V2318P1M.TXT` SAS script.
  - `hcc.py`: the **main** module that combines the various logical components
  - `utils.py`: utility functions for reading data files
- `tests/`: test scripts to check the validity of the outputs.
- `LICENSE.txt`: Apache 2.0.
- `README.md`: This README file.
- `setup.py`: a set-up script.

## Code Examples

`hccpy` is really simple to use.
Please see some examples below:

### Importing 

To import the `HCCEngine` class from `hccpy`:  

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
```

### HCC-Profiling a Member with Diagnosis Codes

To get a HCC profile from a list of diagnosis codes (in ICD-10):

```python
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
```

### HCC-Profiling a New Member

If a member is new, then provide the `elig="NE"` in the input:

```python
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
```

### HCC-Profiling a Intitutionalized Member

If a member has a different eligibility status, change the eligibility as follows (e.g. institutionalized member):

```python
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

## License
Apache 2.0

## Authors
- Yubin Park, PhD

## References
- https://www.nber.org/data/cms-risk-adjustment.html
- https://www.cms.gov/medicare/health-plans/medicareadvtgspecratestats/risk-adjustors.html
- https://github.com/calyxhealth/pyriskadjust
- https://github.com/AlgorexHealth/hcc-python
- https://github.com/galtay/hcc_risk_models
- https://www.cms.gov/cciio/resources/forms-reports-and-other-resources/downloads/ra-march-31-white-paper-032416.pdf


