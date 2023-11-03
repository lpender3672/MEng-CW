C*********************************************************************C
C                                                                     C
C                             gtmain.f                                C
C                                                                     C
C                THERMODYNAMIC ANALYSIS OF OPEN-CIRCUIT               C
C                      GAS TURBINE POWER PLANTS                       C
C                                                                     C
C                        MAIN DRIVER ROUTINE                          C
C                                                                     C
C         (J.B.YOUNG, WHITTLE LABORATORY, CAMBRIDGE, APRIL 1998)      C
C                                                                     C
C              UNIT 1  -  Input datafile.                             C
C              UNIT 2  -  Output of results.                          C
C              UNIT 3  -  Output to plotter.                          C
C              UNIT 5  -  Input from keyboard.                        C
C              UNIT 6  -  Output to VDU.                              C
C                                                                     C
C                       Compile and link with                         C
C      gtplant.f,  modules.f,  gasprops.f,  stmprops.f,  hgraph21     C
C                                                                     C
C*********************************************************************C
C                                                                     C
C     (See the INCLUDE file 'gtinc.f' for a full list of variables.)   C
C                                                                     C
C                                                                     C
C     Gas turbine circuit input dataset :                             C
C                                                                     C
C     TITLE     = Title (maximum 80 characters)                       C
C     REALGS    = .TRUE.  for real gas calculations                   C
C     ICOOLR    = .TRUE.  if intercooler fitted                       C
C     RHEATR    = .TRUE.  if reheater fitted                          C
C     HEATEX    = .TRUE.  if heat exchanger fitted                    C
C     CMPRAT(i) = Pressure ratio of compressor i                      C
C     TBPRAT(i) = Pressure ratio of turbine i                         C
C     ETAC(i)   = Polytropic efficiency of compressor i (0 - 1)       C
C     ETAT(i)   = Polytropic efficiency of turbine i (0 - 1)          C
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
C     Selected output variables :                                     C
C                                                                     C
C     EFFGTO  = Plant overall efficiency based on LCV (0 - 1)         C
C     WGTNET  = Net work output (kJ/kg of exhaust)                    C
C     WGCTOT  = Total Compressor work input (kJ/kg of exhaust)        C
C     WGTTOT  = Total Turbine work output (kJ/kg of exhaust)          C
C     SFCTOT  = Plant specific fuel consumption (kg/kWh)              C
C     TGTEXH  = Exhaust gas temperature (K)                           C
C     CO2EM   = CO2 emission (kg/kWh)                                 C
C     ROX(i)  = Actual / Stoichiometric oxygen for Burner i           C
C     GFR(i)  = Gas / Fuel ratio for Burner i                         C
C                                                                     C
C*********************************************************************C
 
      PROGRAM  MAIN
 
      IMPLICIT REAL*8 (A-H,O-Z)
 
      INCLUDE    'gtinc.f'
 
      REAL*4     X(30,200), Y(30,200),
     &           XMIN, XMAX, YMIN, YMAX, VINCRX, VINCRY
      CHARACTER  XLABL*50, YLABL*50,
     &           LABL1*50, LABL2*50, LABL3*50, XFORM*6, YFORM*6,
     &           INTYPE*1, GRAPH*1, POINTS*1
      LOGICAL    LKBD
 
C=====================================================================C
 
C     Write heading on UNIT 6.
 
      CALL FILESX (0,LKBD)
 
C     Read input data for gas turbine circuit.
 
      CALL GASINP (LKBD)
      WRITE (6,'(/, '' DATA INPUT IS COMPLETE :'')')
 
 
C     SPECIFY NO. OF PLOTS PER GRAPH AND NO. OF CYCLE CALCS PER PLOT :
C     ==============================================================
 
CC      nplot = 1
CC      ncalc = 1
 
C     NOTE (1): Uncomment the following two lines to loop 
C     over design parameters (which are set further below).

      nplot = 8
      ncalc = 25

      DO iplot = 1, nplot

         WRITE (3,3010)
 
C       RESET THE VARIABLES FOR THE NEXT PLOT :
C       =====================================
 
C     NOTE (2): Uncomment the following line to reset 
C     the combustor temperature at each value of iplot.

         TCOMB = 900.0 + (iplot-1)*100.0

         DO icalc = 1, ncalc
 
C         RESET THE VARIABLES FOR THE NEXT CYCLE CALCULATION :
C         ==================================================

C     NOTE (3): Uncomment the following line to reset 
C     the compressor pressure ratio at each value of icalc.
 
          CMPRAT(1) = 5.0 + (icalc-1)*2.5 
 
C         Calculate gas turbine circuit.
 
          IF (REALGS) THEN
            CALL RGCALC
          ELSE
            CALL PGCALC
          ENDIF
 
C         STORE THE RESULTS NEEDED FOR PLOTTING :
C         =====================================

          X(iplot,icalc) = CMPRAT(1)
          Y(iplot,icalc) = EFFGTO * 100.0

C     NOTE (4): ONLY Uncomment the following line when you want to 
C     plot the specific work on the Y-axis. Make sure you also change 
C     the variable YLABL which is set a few lines below.    

          Y(iplot,icalc) = WGTNET / 1000.
 
C     If an error occurs (e.g., an exhaust gas HX cannot be fitted)
C     then fill in the rest of the arrays X() & Y() and exit the loop

          IF (LERR) THEN
            DO i = icalc , ncalc
              X(iplot,i) = X(iplot,icalc-1)
              Y(iplot,i) = Y(iplot,icalc-1)
            ENDDO
            EXIT
          ENDIF

C         Write general results on UNIT 8 (one-off calculations only).
 
          IF (ncalc .EQ. 1) THEN
            CALL GASOUT
            WRITE (6,'(/,'' GAS TURBINE CALCULATION IS COMPLETE.'')')
          ENDIF
 
C     NOTE (5): You can use the following lines (see also the other lines 
C     beginning 'WRITE (3,' above & below) to write out any output you wish 
C     for use with a plotting program of your own choice.

          WRITE (3,3000) TCOMB,CMPRAT(1),EFFGTO*100.,WGTNET/1000.0
 3000     FORMAT (4(E11.5,2X))
 3010     FORMAT ('#',T6,'TIT',T19,'PR',T30,'ETA(%)',T40,'Wnet(kJ/kg)')

C         Plot (T-s) diagram if required (one-off calculations only).
 
          IF (ncalc .EQ. 1) CALL CHDIAG (REALGS)
 
        ENDDO

        WRITE (3,*)
C
      ENDDO
 
 
      IF (ncalc .GT. 1) THEN
 
        WRITE (6,'( /, '' ALL CYCLE CALCULATIONS ARE COMPLETE.'')')
 
C       SPECIFY THE GRAPH FORMAT :
C       ========================
 
C       XLABL  = Label for X-axis (Maximum 50 characters, centralise)
C       YLABL  = Label for Y-axis (Maximum 50 characters, centralise)
C       LABL1  = Description of curves - written at top of graph.
C                (Maximum 50 characters - left justified)
C       LABL2  = As LABL1 but written directly below it.
C       LABL3  = As LABL2 but written directly below it.
C       POINTS = 'Y' - points and line plotted.
C              = 'N' - just a line plotted.
 
        XLABL  = '            Compressor Pressure Ratio             '
C       YLABL  = '             Overall Efficiency (%)               '
        YLABL =  '		Specific Work kW/kg                 '
        LABL1  = 'Curves of constant Turbine Inlet Temperature      '
        LABL2  = '900 - 1600 Celsius.                               '
        LABL3  = '                                                  '
        POINTS = 'Y'
 
C       XMIN   = Minimum value on X-axis.
C       XMAX   = Maximum value on X-axis.
C       VINCRX = Increment between major marks on X-axis.
C       mmarkx = No. of minor marks between major marks on X-axis.
C       XFORM  = Format for X-axis annotation, e.g. '(F7.1)'
 
C       (For automatic X-scaling, set XMIN = XMAX = 0.0)
 
        XMIN   = 0.0
        XMAX   = 65.0
        VINCRX = 10.0
        mmarkx = 9
        XFORM  = '(F5.1)'
 
C       YMIN   = Minimum value on Y-axis.
C       YMAX   = Maximum value on Y-axis.
C       VINCRY = Increment between major marks on Y-axis.
C       mmarky = No. of minor marks between major marks on Y-axis.
C       YFORM  = Format for Y-axis annotation, e.g. '(F7.1)'
 
C       (For automatic Y-scaling, set YMIN = YMAX = 0.0)
 
        YMIN   = 00.0
        YMAX   = 00.0
        VINCRY = 05.0
        mmarky = 9
        YFORM  = '(F7.1)'
 
        DO idiag = 1, 10
          WRITE (6,'(/, '' Do you want to plot a graph ? (y/n)'',
     &                     T60, '':  '', $)')
          READ  (5,'(A1)') GRAPH
          WRITE (6,'(1X)')
          IF ((GRAPH .EQ. 'Y') .OR. (GRAPH .EQ. 'y')) THEN
            CALL GRAPHS (TITLE, XLABL, YLABL, LABL1, LABL2, LABL3,
     &                   POINTS, XMIN, XMAX, YMIN, YMAX,
     &                   VINCRX, VINCRY, mmarkx, mmarky, XFORM, YFORM,
     &                   nplot, ncalc, X, Y)
          ELSE
            GO TO 20
          ENDIF
        ENDDO
 
      ENDIF     
   20 CONTINUE
 
      WRITE (6,'(/, '' JOB IS FINISHED.'', //)')

      CALL FILESX (1,LKBD)
 
      STOP
      END
 
C*********************************************************************C

