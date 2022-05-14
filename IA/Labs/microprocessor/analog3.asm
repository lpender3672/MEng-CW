

        list      p=12f675            ; list directive to define processor
        #include <p12f675.inc>        ; processor specific variable definitions


        errorlevel  -302              ; suppress message 302 from list file

;************************** VARIABLE DEFINITIONS ******************************

        cblock      0x20        ; the first data memory location where variables can be put
        ANALOG_VAL              ; the result of A/D conversion divided by 32 is stored here
        endc                    ; end of variable declarations
        
;****************************** Start of Program ******************************
        org     0x000           ; processor reset vector
        goto    Program_Start

        org     0x005           ; Start of Programm Memory Vector
Program_Start
        
        bsf     STATUS,RP0      ; Bank 1 
	call    0x3ff           ; update factory calibrated oscillator: get the calibration value
        movwf   OSCCAL          ; update factory calibrated oscillator: store it in OSCCAL
        movlw   B'00111111'     ; Set all I/O pins as inputs
        movwf   TRISIO          
        movlw   B'00000001'     ; only use AD0
        movwf   ANSEL
        movlw   B'10000100'     ; Weak pullups: disabled
        movwf   OPTION_REG      ; TMR0 prescaler: 1:32 (TMR0 will overflow in 8.2ms)

        bcf     STATUS,RP0      ; Bank 0
        clrf    GPIO            ; clear all outputs


Main_Loop
        clrwdt                  ; clear Watch Dog Timer

        bcf     STATUS,RP0      ; Bank 0
        movlw   B'00000011'     ; Turn AD converter on and activate
        btfss   ADCON0,1        ; unless it's already converting
        movwf   ADCON0

        movf    ADRESH,W        ; Grab the high 8 bits of the analog result
        movwf   ANALOG_VAL      ; Store it in our own register

        rrf     ANALOG_VAL,f
        rrf     ANALOG_VAL,f    
        rrf     ANALOG_VAL,f    
        rrf     ANALOG_VAL,f    
        rrf     ANALOG_VAL,w    
        andlw   B'00000111'
        movwf   ANALOG_VAL

        bsf     STATUS, RP0     ; Bank 1
        call    Get_Trisio      ; Use lookup table to get the value for the Tristate register
        movwf   TRISIO
        bcf     STATUS, RP0     ; Bank 0
        movf    ANALOG_VAL,w    ; grab analog value again
        call    Get_GPIO        ; Use another lookup table to get the value for the GPIO register
        movwf   GPIO
        goto    Main_Loop       ; go back to main loop

Get_Trisio
        ;; INCOMPLETE LOOKUP TABLE - ENTER YOUR VALUES HERE
        addwf   PCL, f
        retlw   B'00001111'     ; These instructions load a new value into W
        retlw   B'00001111'     ; and return from the function call
        retlw   B'00101011'
        retlw   B'00101011'
        retlw   B'00011011'
        retlw   B'00011011'
        retlw   B'00111001'
        retlw   B'00111001'

Get_GPIO
        ;; INCOMPLETE LOOKUP TABLE - ENTER YOUR VALUES HERE
        addwf   PCL,f
        retlw   B'00010000'
        retlw   B'00100000'
        retlw   B'00010000'
        retlw   B'00000100'
        retlw   B'00100000'
        retlw   B'00000100'
        retlw   B'00000100'
        retlw   B'00000010'

        end