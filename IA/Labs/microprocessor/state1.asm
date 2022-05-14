

        list      p=12f675            ; list directive to define processor
        #include <p12f675.inc>        ; processor specific variable definitions


        errorlevel  -302              ; suppress message 302 from list file

;************************** VARIABLE DEFINITIONS ******************************

        cblock      0x20        ; the first data memory location where variables can be put
        STATE                   ; 0-7 the state of the state machine
        W_STORE                 ; place to store W during interrupt handling
        STATUS_STORE
        endc                    ; end of variable declarations
        
;****************************** Start of Program ******************************
        org     0x000           ; processor reset vector
        goto    Program_Start

        org     0x04
        goto    Interrupt
        
        org     0x005           ; Start of Programm Memory Vector
Program_Start
        
        bsf     STATUS,RP0      ; Set for Bank 1
	call    0x3ff           ; update factory calibrated oscillator: get the calibration value
        movwf   OSCCAL          ; update factory calibrated oscillator: store it in OSCCAL
        movlw   B'00111111'     ; 
        movwf   TRISIO          
        movlw   B'10000111'     ; 
        movwf   OPTION_REG      ; 

        clrf    STATE           ; 
        
        bsf     INTCON,GIE      ; 
        bsf     INTCON,GPIE     ; 
        bsf     IOC,3           ;
        
        bcf     STATUS,RP0      ; 
        clrf    GPIO            ;

Main_Loop
        clrwdt                  ; clear Watch Dog Timer


        bsf     STATUS, RP0     ; Bank 1
        movf    STATE,w         ; get the state value
        call    Get_Trisio      ; Use lookup table to get the value for the Tristate register
        movwf   TRISIO
        bcf     STATUS, RP0     ; Bank 0
        movf    STATE,w         ; get the state value again
        call    Get_GPIO        ; Use another lookup table to get the value for the GPIO register
        movwf   GPIO
        goto    Main_Loop       ; go back to main loop

Get_Trisio
        ;; Lookup table trick
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
        ;; Lookup table trick again
        addwf   PCL,f
        retlw   B'00010000'
        retlw   B'00100000'
        retlw   B'00010000'
        retlw   B'00000100'
        retlw   B'00100000'
        retlw   B'00000100'
        retlw   B'00000100'
        retlw   B'00000010'


Interrupt
        movwf   W_STORE         ; keep the value of W
        swapf   STATUS,w
        movwf   STATUS_STORE    ; status is stored in nybble reversed format
                
        bcf     STATUS,RP0      ; Bank 0
        movf    GPIO,f          ; hit the GPIO to clear any key changed events
        bcf     INTCON,GPIF

        btfsc   GPIO,3          ; If it wasn't a press event
        goto    Interrupt_Return ; the just return from interrupt
        
        ;;  increment the state (and reset to zero if it overflowed)
        incf    STATE,w
        andlw   0x07
        movwf   STATE

        
Interrupt_Return        
        swapf   STATUS_STORE,w
        movwf   STATUS
        swapf   W_STORE,f
        swapf   W_STORE,w
        retfie
        
        end