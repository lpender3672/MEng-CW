

        list      p=12f675            ; list directive to define processor
        #include <p12f675.inc>        ; processor specific variable definitions


        errorlevel  -302              ; suppress message 302 from list file

;************************** VARIABLE DEFINITIONS ******************************

        cblock      0x20        ; the first data memory location where variables can be put
        LED                     ; 0-7 which LED is lit up.
        W_STORE                 ; place to store W during interrupt handling
        STATUS_STORE
        DEBOUNCE_STATE
        endc                    ; end of variable declarations

;****************************** Start of Program ******************************
        org     0x000           ; processor reset vector
        goto    Program_Start

        org     0x04
        goto    Interrupt
        
        org     0x005           ; Start of Programm Memory Vector
Program_Start
        clrf    DEBOUNCE_STATE  ; Waiting for a button press
        
        bsf     STATUS,RP0      ; Bank 1 
	call    0x3ff           ; update factory calibrated oscillator: get the calibration value
        movwf   OSCCAL          ; update factory calibrated oscillator: store it in OSCCAL
        movlw   B'00111111'     ; Set all I/O pins as inputs
        movwf   TRISIO

        ;; Weak pullups disabled
        ;; TMR0 prescaler: 1:256 (TMR0 will overflow in 64ms)
        movlw   B'10000111'     ;
        movwf   OPTION_REG      ;

        clrf    LED             ;Start with LED 0
        
        bsf     INTCON,GIE      ; Enable interrupts
        bsf     INTCON,GPIE     ; Enable interrupt on GPIO change
        bsf     INTCON,T0IE     ; Enable interrupt on Timer 0
        bsf     IOC,3           ; Enable interrupts on GP3 (the switch)
        
        bcf     STATUS,RP0      ; Bank 0
        clrf    GPIO            ; clear all outputs

Main_Loop
        nop
	goto Main_Loop
