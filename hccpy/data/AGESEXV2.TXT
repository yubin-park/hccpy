 %MACRO AGESEXV2(AGEF=, SEX=, OREC=);
 %**********************************************************************
 ***********************************************************************
  1  MACRO NAME:     AGESEXV2
  2  PURPOSE:        create demographic variables used in regressions.
  3  PARAMETERS:
                     AGEF     - age variable (integer)
                     SEX      - sex variable (character)
                     OREC     - original reason for entitlement
                                variable from Denominator (character)
  4  CREATED VARIABLES:
                     ORIGDS  - originally disabled dummy variable
                     DISABL  - disabled dummy variable
                     24 dummy agesex variables for all models except
                     "new enrollee":
                     F0_34  F35_44 F45_54 F55_59 F60_64 F65_69
                     F70_74 F75_79 F80_84 F85_89 F90_94 F95_GT
                     M0_34  M35_44 M45_54 M55_59 M60_64 M65_69
                     M70_74 M75_79 M80_84 M85_89 M90_94 M95_GT
                     32 dummy agesex variables for "new enrollee" model:
                     NEF0_34  NEF35_44 NEF45_54 NEF55_59 NEF60_64
                     NEF65    NEF66    NEF67    NEF68    NEF69
                     NEF70_74 NEF75_79 NEF80_84 NEF85_89 NEF90_94
                     NEF95_GT
                     NEM0_34  NEM35_44 NEM45_54 NEM55_59 NEM60_64
                     NEM65    NEM66    NEM67    NEM68    NEM69
                     NEM70_74 NEM75_79 NEM80_84 NEM85_89 NEM90_94
                     NEM95_GT
 ***********************************************************************;
      LENGTH
              /* for all score variables except "NEW ENROLLEE" */
              F0_34  F35_44 F45_54 F55_59 F60_64 F65_69
              F70_74 F75_79 F80_84 F85_89 F90_94 F95_GT
              M0_34  M35_44 M45_54 M55_59 M60_64 M65_69
              M70_74 M75_79 M80_84 M85_89 M90_94 M95_GT
              DISABL
              ORIGDS
              /* for "NEW ENROLLEE" score variable */
              NEF0_34  NEF35_44 NEF45_54 NEF55_59 NEF60_64
              NEF65    NEF66    NEF67    NEF68    NEF69
              NEF70_74 NEF75_79 NEF80_84 NEF85_89 NEF90_94
              NEF95_GT
              NEM0_34  NEM35_44 NEM45_54 NEM55_59 NEM60_64
              NEM65    NEM66    NEM67    NEM68    NEM69
              NEM70_74 NEM75_79 NEM80_84 NEM85_89 NEM90_94
              NEM95_GT
            3.;

       /* for all score variables except "NEW ENROLLEE" */
      ARRAY   CELL(24)
              F0_34  F35_44 F45_54 F55_59 F60_64 F65_69
              F70_74 F75_79 F80_84 F85_89 F90_94 F95_GT
              M0_34  M35_44 M45_54 M55_59 M60_64 M65_69
              M70_74 M75_79 M80_84 M85_89 M90_94 M95_GT
              ;
       /* for "NEW ENROLLEE" score variable */
      ARRAY NECELL(32)
              NEF0_34  NEF35_44 NEF45_54 NEF55_59 NEF60_64
              NEF65    NEF66    NEF67    NEF68    NEF69
              NEF70_74 NEF75_79 NEF80_84 NEF85_89 NEF90_94 NEF95_GT
              NEM0_34  NEM35_44 NEM45_54 NEM55_59 NEM60_64
              NEM65    NEM66    NEM67    NEM68    NEM69
              NEM70_74 NEM75_79 NEM80_84 NEM85_89 NEM90_94 NEM95_GT
              ;
 %**********************************************************************
 *  disabled, originally disabled variables
 ***********************************************************************;

       %* disabled;
       DISABL = (&AGEF < 65 & &OREC ne "0");
       %* originally disabled: CHANGED FIRST TIME FOR THIS SOFTWARE;
       ORIGDS  = (&OREC = '1')*(DISABL = 0);

 %**********************************************************************
 * variables for all models exept "new enrollee"
 ***********************************************************************;

       SELECT;
         WHEN(&SEX='2' & 0<= &AGEF <=34) _AGESEX  = 1;
         WHEN(&SEX='2' & 34< &AGEF <=44) _AGESEX  = 2;
         WHEN(&SEX='2' & 44< &AGEF <=54) _AGESEX  = 3;
         WHEN(&SEX='2' & 54< &AGEF <=59) _AGESEX  = 4;
         WHEN(&SEX='2' & 59< &AGEF <=64) _AGESEX  = 5;
         WHEN(&SEX='2' & 64< &AGEF <=69) _AGESEX  = 6;
         WHEN(&SEX='2' & 69< &AGEF <=74) _AGESEX  = 7;
         WHEN(&SEX='2' & 74< &AGEF <=79) _AGESEX  = 8;
         WHEN(&SEX='2' & 79< &AGEF <=84) _AGESEX  = 9;
         WHEN(&SEX='2' & 84< &AGEF <=89) _AGESEX  = 10;
         WHEN(&SEX='2' & 89< &AGEF <=94) _AGESEX  = 11;
         WHEN(&SEX='2' & &AGEF >94)      _AGESEX  = 12;
         WHEN(&SEX='1' & 0<= &AGEF <=34) _AGESEX  = 13;
         WHEN(&SEX='1' & 34< &AGEF <=44) _AGESEX  = 14;
         WHEN(&SEX='1' & 44< &AGEF <=54) _AGESEX  = 15;
         WHEN(&SEX='1' & 54< &AGEF <=59) _AGESEX  = 16;
         WHEN(&SEX='1' & 59< &AGEF <=64) _AGESEX  = 17;
         WHEN(&SEX='1' & 64< &AGEF <=69) _AGESEX  = 18;
         WHEN(&SEX='1' & 69< &AGEF <=74) _AGESEX  = 19;
         WHEN(&SEX='1' & 74< &AGEF <=79) _AGESEX  = 20;
         WHEN(&SEX='1' & 79< &AGEF <=84) _AGESEX  = 21;
         WHEN(&SEX='1' & 84< &AGEF <=89) _AGESEX  = 22;
         WHEN(&SEX='1' & 89< &AGEF <=94) _AGESEX  = 23;
         WHEN(&SEX='1' & &AGEF > 94)     _AGESEX  = 24;
         OTHERWISE;
       END;
       DO _I=1 TO 24;
          CELL(_I) = (_AGESEX  = _I);
       END;

 %**********************************************************************
 * age/sex vars for "new enrollee"  model
 ***********************************************************************;
       SELECT;
           WHEN(&SEX='2' & 0<= &AGEF <=34) NE_AGESEX = 1;
           WHEN(&SEX='2' & 34< &AGEF <=44) NE_AGESEX = 2;
           WHEN(&SEX='2' & 44< &AGEF <=54) NE_AGESEX = 3;
           WHEN(&SEX='2' & 54< &AGEF <=59) NE_AGESEX = 4;
           WHEN(&SEX='2' & 59< &AGEF <=63) NE_AGESEX = 5;
           WHEN(&SEX='2' & &AGEF=64 & &OREC NE '0') NE_AGESEX = 5;
           WHEN(&SEX='2' & &AGEF=64 & &OREC='0')    NE_AGESEX = 6;
           WHEN(&SEX='2' &    &AGEF  =65)  NE_AGESEX = 6;
           WHEN(&SEX='2' &    &AGEF  =66)  NE_AGESEX = 7;
           WHEN(&SEX='2' &    &AGEF  =67)  NE_AGESEX = 8;
           WHEN(&SEX='2' &    &AGEF  =68)  NE_AGESEX = 9;
           WHEN(&SEX='2' &    &AGEF  =69)  NE_AGESEX = 10;
           WHEN(&SEX='2' & 69< &AGEF <=74) NE_AGESEX = 11;
           WHEN(&SEX='2' & 74< &AGEF <=79) NE_AGESEX = 12;
           WHEN(&SEX='2' & 79< &AGEF <=84) NE_AGESEX = 13;
           WHEN(&SEX='2' & 84< &AGEF <=89) NE_AGESEX = 14;
           WHEN(&SEX='2' & 89< &AGEF <=94) NE_AGESEX = 15;
           WHEN(&SEX='2' & &AGEF >94)      NE_AGESEX = 16;
           WHEN(&SEX='1' & 0<= &AGEF <=34) NE_AGESEX = 17;
           WHEN(&SEX='1' & 34< &AGEF <=44) NE_AGESEX = 18;
           WHEN(&SEX='1' & 44< &AGEF <=54) NE_AGESEX = 19;
           WHEN(&SEX='1' & 54< &AGEF <=59) NE_AGESEX = 20;
           WHEN(&SEX='1' & 59< &AGEF <=63) NE_AGESEX = 21;
           WHEN(&SEX='1' & &AGEF=64 & &OREC NE '0') NE_AGESEX = 21;
           WHEN(&SEX='1' & &AGEF=64 & &OREC='0')   NE_AGESEX = 22;
           WHEN(&SEX='1' &     &AGEF  =65) NE_AGESEX = 22;
           WHEN(&SEX='1' &     &AGEF  =66) NE_AGESEX = 23;
           WHEN(&SEX='1' &     &AGEF  =67) NE_AGESEX = 24;
           WHEN(&SEX='1' &     &AGEF  =68) NE_AGESEX = 25;
           WHEN(&SEX='1' &     &AGEF  =69) NE_AGESEX = 26;
           WHEN(&SEX='1' & 69< &AGEF <=74) NE_AGESEX = 27;
           WHEN(&SEX='1' & 74< &AGEF <=79) NE_AGESEX = 28;
           WHEN(&SEX='1' & 79< &AGEF <=84) NE_AGESEX = 29;
           WHEN(&SEX='1' & 84< &AGEF <=89) NE_AGESEX = 30;
           WHEN(&SEX='1' & 89< &AGEF <=94) NE_AGESEX = 31;
           WHEN(&SEX='1' & &AGEF >94)      NE_AGESEX = 32;
           OTHERWISE;
       END;
       DO _I=1 TO 32;
           NECELL(_I)=(NE_AGESEX=_I);
       END;

 %**********************************************************************;
       LABEL
       ORIGDS ="originally disabled dummy variable"
       DISABL ="disabled dummy variable"
      ;

 %MEND AGESEXV2;
