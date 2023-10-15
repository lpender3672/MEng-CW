C*********************************************************************C
C                                                                     C
C                               gt.inc                                C
C                                                                     C
C                THERMODYNAMIC ANALYSIS OF OPEN-CIRCUIT               C
C                      GAS TURBINE POWER PLANTS                       C
C                                                                     C
C                           INCLUDE FILE                              C
C                                                                     C
C         (J.B.YOUNG, WHITTLE LABORATORY, CAMBRIDGE, APRIL 1998)      C
C                                                                     C
C*********************************************************************C
C                                                                     C
C     Description of variables held in COMMON :                       C
C                                                                     C
C                                                                     C
C     COMMON /GT1/ contains the complete input dataset :              C
C                                                                     C
C     TITLE     = Title (maximum 80 characters)                       C
C     REALGS    = .TRUE.  for real gas calculations                   C
C     ICOOLR    = .TRUE.  if intercooler fitted                       C
C     RHEATR    = .TRUE.  if reheater fitted                          C
C     HEATEX    = .TRUE.  if heat exchanger fitted                    C
C     CMPRAT(i) = Pressure ratio of compressor i                      C
C     TBPRAT(i) = Pressure ratio of turbine i                         C
C     ETAC(i)   = Isentropic efficiency of compressor i (0 - 1)       C
C     ETAT(i)   = Isentropic efficiency of turbine i (0 - 1)          C
C     FCOOL(i)  = Fractional cooling flow for turbine i               C
C     PCOOL(i)  = Mixing point (fraction of pressure drop in turbine) C
C     EFFRHX    = Effectiveness of heat exchanger (0 - 1)             C
C     MFUEL(i)  = Mass fraction of element i in fuel :                C
C                 i = 1 (N), 2 (O), 3 (H), 4 (C), 5 (Ash)             C
C     LCV       = Lower calorific value of fuel (MJ/kg)               C
C     PATMOS    = Atmospheric pressure (bar)                          C
C     TATMOS    = Atmospheric temperature (C)                         C
C     TINTC     = Temperature after intercooler (C)                   C
C     TCOMB     = Temperature after main combustion chamber (C)       C
C     TRHTR     = Temperature after reheater (C)                      C
C     FPINTC    = Fractional pressure loss in intercooler             C
C     FPCOMB    = Fractional pressure loss in combustion chamber      C
C     FPRHTR    = Fractional pressure loss in reheater                C
C     FPRHXC    = Fractional pressure loss in recuperator (cold side) C
C     FPRHXH    = Fractional pressure loss in recuperator (hot side)  C
C     CP1       = Cp for compressor (J/kgK)  - Perfect gas calcs.     C
C     GA1       = Gamma for compressor       - Perfect gas calcs.     C
C     CP2       = Cp for products (J/kgK)    - Perfect gas calcs.     C
C     GA2       = Gamma for products         - Perfect gas calcs.     C
C                                                                     C
C                                                                     C
C     COMMON /GT2/ contains the properties around the circuit :       C
C                                                                     C
C     Row 1, P** = Pressure (N/m**2)                                  C
C     Row 2, T** = Temperature (K)                                    C
C     Row 3, D** = Density (kg/m**3)                                  C
C     Row 4, H** = Specific enthalpy (J/kg)                           C
C     Row 5, S** = Specific entropy (J/kgK)                           C
C     Row 6, R** = Specific gas constant (J/kgK)                      C
C     Row 7, C** = Isobaric specific heat (J/kgK)                     C
C     Row 8, G** = Isentropic exponent                                C
C     Row 9, F** = Flowrate (fraction of exhaust flow)                C
C                                                                     C
C     Col 1, *GC(i,j) = Compressor i                                  C
C                       (j = 1 inlet, j = 2 outlet)                   C
C     Col 2, *GT(i,j) = Turbine i                                     C
C                       (j = 1 inlet, j = 2 outlet)                   C
C     Col 3, *BN(i,j) = Burner i                                      C
C                       (j = 1 inlet, j = 2 outlet)                   C
C     Col 4, *MX(i,j) = Mixing of coolant in Turbine i                C
C                       (j = 1 upstream in turbine)                   C
C                       (j = 2 after mixing in turbine)               C
C                       (j = 3 coolant flow after throttling)         C
C     Col 5, *HX(j)   = Heat exchanger                                C
C                       (j = 1 inlet, j = 2 outlet, cold side)        C
C                       (j = 3 inlet, j = 4 outlet, hot side)         C
C     Col 6, *ST(j)   = Standard state (1 bar, 25 Celsius)            C
C                       (j = 1 inlet, j = 2 exhaust)                  C
C                                                                     C
C                                                                     C
C     COMMON /GT3/ contains miscellaneous gas data :                  C
C                                                                     C
C     MFGC(i,j,k) = Gas mol fractions, Compressor i                   C
C     MFGT(i,j,k) = Gas mol fractions, Turbine i                      C
C     MFBN(i,j,k) = Gas mol fractions, Burner i                       C
C     MFMX(i,k)   = Gas mol fractions, Mixing in Turbine i            C
C     MFHX(j,k)   = Gas mol fractions, Heat exchanger                 C
C                   k = 1 (N2),  2 (O2),  3 (H2O),  4 (CO2)           C
C     MDH0        = -DHo (J/kg)                                       C
C     MDG0        = -DGo (J/kg)                                       C
C     TGTEXH      = Exhaust gas temperature (K)                       C
C     ROX(i)      = Actual / Stoichiometric oxygen for Burner i       C
C     GFR(i)      = Gas / Fuel ratio for Burner i                     C
C     GC1         = R for compressor (J/kgK) - Perfect gas calcs.     C
C     GC2         = R for products (J/kgK)   - Perfect gas calcs.     C
C     ngc         = Number of compressors                             C
C     ngt         = Number of turbines                                C
C                                                                     C
C                                                                     C
C     COMMON /ENG/ contains efficiencies, work and heat terms, etc :  C
C     (All work, heat and exergy terms in J/kg of exhaust gas)        C
C                                                                     C
C     EFFGTO  = Plant overall efficiency based on LCV (0 - 1)         C
C     WGTNET  = Net work output                                       C
C     WGCTOT  = Total Compressor work input                           C
C     WGTTOT  = Total Turbine work output                             C
C     SFCTOT  = Plant specific fuel consumption (kg/kWh)              C
C     SFC(i)  = SFC for Burner i (kg/kWh)                             C
C     CO2EM   = CO2 emission (kg/kWh)                                 C
C     EBNTOT  = Total energy input to plant                           C
C     EBN(i)  = Energy input, Burner i                                C
C     WGC(i)  = Work input, Compressor i                              C
C     WGT(i)  = Work output, Turbine i                                C
C     QICTOT  = Heat out, Intercooler                                 C
C     QAIRIN  = Enthalpy of inlet air (above 25 C)                    C
C     QEXHST  = Enthalpy of exhaust gas (above 25 C)                  C
C     QRHX    = Heat transferred in Heat Exchanger                    C
C     EGTOUT  = Total energy output from plant                        C
C     WGTMAX  = Total exergy input to plant                           C
C     WGTM(i) = Exergy input, Burner i                                C
C     WLGC(i) = Lost work, Compressor i                               C
C     WLGT(i) = Lost work, Turbine i                                  C
C     WLGB(i) = Lost work, Burner i                                   C
C     WLCT(i) = Lost work, Coolant Throttling, Turbine i              C
C     WLMX(i) = Lost work, Coolant Mixing, Turbine i                  C
C     WLGIC   = Lost work, Intercooler                                C
C     WLGIN   = Lost work, Inlet Air (zero at 25 C)                   C
C     WLGEXH  = Lost work, Exhaust Gas                                C
C     WLGRHX  = Lost work, Heat Exchanger                             C
C     WLGSUM  = Total lost work                                       C
C                                                                     C
C*********************************************************************C

      COMMON /GT1/ REALGS, ICOOLR, RHEATR, HEATEX, 
     &             CMPRAT(2), ETAC(2), MFUEL(5),
     &             TBPRAT(2), ETAT(2), FCOOL(2), PCOOL(2),
     &             TINTC, TCOMB, TRHTR, PATMOS, TATMOS,
     &             FPINTC, FPCOMB, FPRHTR, FPRHXC, FPRHXH,
     &             CP1, GA1, CP2, GA2, LCV, EFFRHX, TITLE, LERR
      REAL*8       MFUEL, LCV
      CHARACTER    TITLE*80
      LOGICAL      REALGS, ICOOLR, RHEATR, HEATEX, LERR

      COMMON /GT2/ PGC(2,2),PGT(2,2),PBN(2,2),PMX(2,3),PHX(4),PST(2),
     &             TGC(2,2),TGT(2,2),TBN(2,2),TMX(2,3),THX(4),TST(2),
     &             DGC(2,2),DGT(2,2),DBN(2,2),DMX(2,3),DHX(4),DST(2),
     &             HGC(2,2),HGT(2,2),HBN(2,2),HMX(2,3),HHX(4),HST(2),
     &             SGC(2,2),SGT(2,2),SBN(2,2),SMX(2,3),SHX(4),SST(2),
     &             RGC(2,2),RGT(2,2),RBN(2,2),RMX(2,3),RHX(4),RST(2),
     &             CGC(2,2),CGT(2,2),CBN(2,2),CMX(2,3),CHX(4),CST(2),
     &             GGC(2,2),GGT(2,2),GBN(2,2),GMX(2,3),GHX(4),GST(2),
     &             FGC(2,2),FGT(2,2),FBN(2,2),FMX(2,3),FHX(4),FST(2)

      COMMON /GT3/ MFGC(2,2,4), MFGT(2,2,4), MFBN(2,2,4),
     &             MFMX(2,2,4), MFHX(4,4), ROX(2), GFR(2),
     &             MDH0, MDG0, TGTEXH, GC1, GC2, ngc, ngt
      REAL*8       MFGC, MFGT, MFBN, MFMX, MFHX, MDH0, MDG0

      COMMON /ENG/ EFFGTO,  WGTNET,  WGCTOT,  WGTTOT,  CO2EM, SFCTOT,
     &             EBNTOT,  EBN(2),  WGC(2),  WGT(2),  SFC(2),
     &             QICTOT,  QAIRIN,  QEXHST,  QRHX,    EGTOUT,
     &             WGTMAX,  WGTM(2), WLGC(2), WLGT(2), WLGB(2),
     &             WLCT(2), WLMX(2), WLGIC,   WLGIN,   WLGEXH,
     &             WLGRHX,  WLGSUM

      COMMON /GPE/ RMOL, AMASS(4), SYMBEL(4)
      COMMON /GPS/ AC(5,4),  MOLWT(4), CPOR(4), SOR(4),
     &             HFORM(4), GFORM(4), SYMBSP(4)
      REAL*8       MOLWT
      CHARACTER    SYMBEL*2, SYMBSP*6

C*********************************************************************C

