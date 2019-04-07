
def get_ds(age, orec, medicaid, elig):

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

    return disabled, origds, elig  




