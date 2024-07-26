
def get_ds(age, orec, medicaid, elig):

    disabled = 0
    if age < 65 and orec != "0":
        disabled = 1
    origds = 0
    if orec in ("1") and disabled == 0:
        origds = 1
    origesrd = 0
    if orec in ("2", "3") and disabled == 0:
        origesrd = 1
    if elig in {"NE", "SNPNE"}:
        if medicaid:
            elig += "_MCAID"
        else:
            elig += "_NMCAID"
        if origds > 0:
            elig += "_ORIGDIS_NE"
        else:
            elig += "_NORIGDIS_NE"

    return disabled, origds, origesrd, elig




