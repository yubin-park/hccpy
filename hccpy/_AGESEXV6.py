
def get_agesex(age, sex):

    agegroup = "Adult"
    agesexvar = "MAGE_LAST_21_24" 

    if age < 1:
        agesexvar = sex + "AGE_LAST_0_0"
        if sex == "M": 
            agesexvar = "AGE0_MALE" 
        agegroup = "Infant"
    elif age < 2:
        agesexvar = sex + "AGE_LAST_1_1"
        if sex == "M":
            agesexvar = "AGE1_MALE"
        agegroup = "Infant"
    elif age < 5:
        agegroup = "Child"
        agesexvar = sex + "AGE_LAST_2_4"
    elif age < 10:
        agegroup = "Child"
        agesexvar = sex + "AGE_LAST_5_9"
    elif age < 15:
        agegroup = "Child"
        agesexvar = sex + "AGE_LAST_10_14"
    elif age < 21:
        agegroup = "Child"
        agesexvar = sex + "AGE_LAST_15_20"
    elif age < 25:
        agegroup = "Adult"
        agesexvar = sex + "AGE_LAST_21_24"
    elif age < 30:
        agegroup = "Adult"
        agesexvar = sex + "AGE_LAST_25_29"
    elif age < 35:
        agegroup = "Adult"
        agesexvar = sex + "AGE_LAST_30_34"
    elif age < 40:
        agegroup = "Adult"
        agesexvar = sex + "AGE_LAST_35_39"
    elif age < 45:
        agegroup = "Adult"
        agesexvar = sex + "AGE_LAST_40_44"
    elif age < 50:
        agegroup = "Adult"
        agesexvar = sex + "AGE_LAST_45_49"
    elif age < 55:
        agegroup = "Adult"
        agesexvar = sex + "AGE_LAST_50_54"
    elif age < 60:
        agegroup = "Adult"
        agesexvar = sex + "AGE_LAST_55_59"
    else:
        agegroup = "Adult"
        agesexvar = sex + "AGE_LAST_60_GT"

    return agesexvar, agegroup




