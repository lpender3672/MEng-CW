

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

        movlw  B'00000010'
        movwf BINTS

        clrf    LED             ;Start with LED 0
        
        bsf     INTCON,GIE      ; Enable interrupts
        bsf     INTCON,GPIE     ; Enable interrupt on GPIO change
        bsf     INTCON,T0IE     ; Enable interrupt on Timer 0
        bsf     IOC,3           ; Enable interrupts on GP3 (the switch)
        
        bcf     STATUS,RP0      ; Bank 0
        clrf    GPIO            ; clear all outputs

Main_Loop
        clrwdt                  ; clear Watch Dog Timer


        bsf     STATUS, RP0     ; Bank 1
        movf    LED,w
        call    Get_Trisio      ; Use lookup table to get the value for the Tristate register
        movwf   TRISIO
        bcf     STATUS, RP0     ; Bank 0
        movf    LED,w           ; grab LED value again
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

        bcf     STATUS, RP0
        movf    GPIO, f
        
        ;What caused the interrupt?
        btfsc   INTCON, T0IF
        goto    timer_interrupt
        goto    button_interrupt

        
timer_interrupt
        bcf     INTCON, T0IF         ;Clear interrupt

        movf    DEBOUNCE_STATE, w    ;The next action depends on the current state
        addwf   PCL, f
        goto    Interrupt_Return
        goto    increment_state 
        goto    increment_state 
        goto    reset_debounce 

button_interrupt
        
        decfsz  BINTS,1
        goto button_set
        movlw  B'00000010'
        movwf BINTS
        goto Interrupt_Return

button_set
        bcf     INTCON, GPIF         ; Clear interrupt
        movf    DEBOUNCE_STATE, w    ;The next action depends on the current state
        addwf   PCL, f
        goto    advance_led
        goto    Interrupt_Return 
        goto    Interrupt_Return
        goto    Interrupt_Return
    

reset_debounce:
        clrf    DEBOUNCE_STATE
        goto    Interrupt_Return;

advance_led:
        incf    LED,w                   ;Advance the LED
        andlw   0x07
        movwf   LED

        movlw  1                        ;Move to state 1
        movwf  DEBOUNCE_STATE
        goto   Interrupt_Return

increment_state:
        incf    DEBOUNCE_STATE, f
        goto    Interrupt_Return

Interrupt_Return        

        swapf   STATUS_STORE,w
        movwf   STATUS
        swapf   W_STORE,f
        swapf   W_STORE,w
        retfie
        
        end