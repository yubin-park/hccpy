def get_risk_dct(coefn, hcc_lst, age, sex, elig, origds, origesrd, full_partial_nondual, disabled, lti, graft_duration):

    risk_dct = {}

    # build demographic bracket strings and add to risk_dct
    
    if elig in {"DI", "GI",}:
        elig_sex = elig + "_" + sex
    elif elig in {'GF','GNP'}:
        # broken out by aged and non aged
        aged = 'N' if disabled else 'A'
        elig += aged
        elig_sex = elig + "_" + sex
    elif elig in {'DNE', 'GNE'}:
        # new enrolle
        elig_sex = "NE" + sex
    elif elig in {"TRANSPLANT_KIDNEY_ONLY_1M",
                  "TRANSPLANT_KIDNEY_ONLY_2M",
                  "TRANSPLANT_KIDNEY_ONLY_3M"}:
        elig_sex = elig

    

    # build age bracket strings and add to risk_dct
    # ESRD new enrolee age variables do not follow samme structure
    
    if elig == 'GNE' and 65 <= age <= 69:
        age_match = elig_sex + str(age)
    elif elig in {"TRANSPLANT_KIDNEY_ONLY_1M",
                  "TRANSPLANT_KIDNEY_ONLY_2M",
                  "TRANSPLANT_KIDNEY_ONLY_3M"}:
        age_match = elig_sex
    else:
        age_ranges = [x for x in coefn.keys() if elig_sex in x and elig in x and '_' in x[-5:]]
        if not age_ranges:
            print('\t',elig)
            print('\t',disabled)
            print('\t',elig_sex)
            print('\t',age_ranges)
        age_match = ""
        for age_range in age_ranges:

            age_tokens = age_range[-5:].replace(sex, "").split("_") 
            lb, ub = 0, 999 
            if len(age_tokens) == 1:
                lb = int(age_tokens[0])
                ub = lb + 1
            elif age_tokens[1] == "GT":
                lb = int(age_tokens[0])
            else: 
                lb = int(age_tokens[0])
                ub = int(age_tokens[1]) + 1
            if lb <= age < ub:
                if elig in {'DNE', 'GNE'}:
                    age_match = elig_sex + age_range.split(elig_sex)[1]
                else:
                    age_match = age_range
                break

    # Dual status interactions with Age and Sex used in dialysis CE model;
    elig_fbpb = ''
    if elig == "DI" and full_partial_nondual != 'N':
        if full_partial_nondual == 'F':
            elig_fbpb = elig + '_FBDual'
        else:
            elig_fbpb = elig + '_PBDual'
        if sex == 'M':
            elig_fbpb += '_Male'
        else:
            elig_fbpb += '_Female'
        if disabled:
            elig_fbpb += '_NonAged'
        else:
            elig_fbpb += '_Aged'
        
    # Originally Disabled Interactions with Sex used in dialysis CE model and functioning graft community aged models;
    elig_origds = ''
    if origds > 0:
        elig_origds = elig + "_OriginallyDisabled_"
        if sex == "M":
            elig_origds += "Male"
        else:
            elig_origds += "Female"
        
    # Originally ESRD interactions with Sex used in dialysis CE model;
    elig_origesrd = ''
    if elig == 'DI' and origesrd > 0:
        elig_origesrd = elig + "_Originally_ESRD_"
        if sex == "M":
            elig_origesrd += "Male"
        else:
            elig_origesrd += "Female"
            
    # LTI interactions with Aged used in dialysis CE model;
    elig_ltia = ''
    if elig == "DI" and lti > 0:
        elig_ltia = elig + '_LTI_'
        if disabled:
            elig_ltia += 'NonAged'
        else:
            elig_ltia += 'Aged'

    # dualstatus (ND_PBD / FBD), origds (NORIGDIS / ORIGDIS), modelcode ('', G), sex_age_band (== age_match)

    base_demo_variable = ''
    if elig in {'DNE', 'GNE'}:
        base_demo_variable = '_'.join([
            elig,
            'FBD' if full_partial_nondual == 'F' else 'ND_PBD',
            'ORIGDIS' if origds > 0 else 'NORIGDIS',
            age_match if elig == 'DNE' else 'G_' + age_match
        ])
    else:
        base_demo_variable = age_match

    fgf_variable = '' # functioning graft factor transplant bump-up factors
    pbd_factor_variable = '' # partial benefit dual status bump up factors
    actadj_variable = ''
    if 'G' in elig:
        if graft_duration:
            fgf_variable = '_'.join([
                'FGI' if lti > 0 else 'FGC',
                'LT65' if disabled > 0 else 'GE65',
                graft_duration,
                'FBD' if full_partial_nondual == 'F' else 'ND_PBD',
            ])
        if full_partial_nondual == 'P' and not 'NE' in elig:
            pbd_factor_variable = '_'.join([
                'FGI' if lti > 0 else 'FGC',
                'PBD',
                'LT65' if disabled > 0 else 'GE65',
                'flag'
            ])

        # Actuarial adjustment factor for new enrollees functioning graft model transplant bumps
        if elig == 'GNE' and graft_duration:
            actadj_variable = 'ActAdj_'
            actadj_variable += graft_duration
    
    actadj_factor = coefn.get(actadj_variable, 1.0)
    
    if base_demo_variable:
        risk_dct[base_demo_variable] = coefn.get(base_demo_variable, 0.0)

    if elig_fbpb:
        risk_dct[elig_fbpb] = coefn.get(elig_fbpb, 0.0)

    if elig_origds:
        risk_dct[elig_origds] = coefn.get(elig_origds, 0.0)

    if elig_origds:
        risk_dct[elig_origds] = coefn.get(elig_origds, 0.0)

    if elig_ltia:
        risk_dct[elig_ltia] = coefn.get(elig_ltia, 0.0)

    if fgf_variable:
        risk_dct[fgf_variable] = coefn.get(fgf_variable, 0.0)

    if pbd_factor_variable:
        risk_dct[pbd_factor_variable] = coefn.get(pbd_factor_variable, 0.0)

    
    # # build hcc factor strings and add to risk_dict
    for hcc in hcc_lst:
        elig_hcc = elig + '_' + hcc
        risk_dct[elig_hcc] = coefn.get(elig_hcc, 0.0)

    return risk_dct, actadj_factor