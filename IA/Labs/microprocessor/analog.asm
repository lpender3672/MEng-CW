        ;; an analog indicator program

        list      p=12f675      ; list directive to define processor
        #include <p12f675.inc>  ; processor specific variable definitions
        errorlevel  -302        ; suppress message 302 from list file

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

        ;; divide the result of the analog conversion by 32
        ;; 
        rrf     ANALOG_VAL,f    ; divide by 2
        rrf     ANALOG_VAL,f    ; again
        rrf     ANALOG_VAL,f    ; again
        rrf     ANALOG_VAL,f    ; again
        rrf     ANALOG_VAL,w    ; again but store the result in W this time
        andlw   B'00000111'     ; get rid of the high bits we don't want
        movwf   ANALOG_VAL      ; and store the result back in memory

        ;; compare result to 0
        movlw   0
        subwf   ANALOG_VAL,w    ; subtract 0 from value
        btfsc   STATUS,Z        ; test the zero flag in STATUS, if set we execute the next instruction
        goto    LED0            ; which takes us to turning on LED0

        ;; compare result to 1
        movlw   1
        subwf   ANALOG_VAL,w    ; subtract 1 from value
        btfsc   STATUS,Z
        goto    LED1

        ;; and so on
        movlw   2
        subwf   ANALOG_VAL,w
        btfsc   STATUS,Z
        goto    LED2
        
        movlw   3
        subwf   ANALOG_VAL,w
        btfsc   STATUS,Z
        goto    LED3

        movlw   4
        subwf   ANALOG_VAL,w
        btfsc   STATUS,Z
        goto    LED4

        movlw   5
        subwf   ANALOG_VAL,w
        btfsc   STATUS,Z
        goto    LED5

        movlw   6
        subwf   ANALOG_VAL,w
        btfsc   STATUS,Z
        goto    LED6

        movlw   7
        subwf   ANALOG_VAL,w
        btfsc   STATUS,Z
        goto    LED7

        goto    Main_Loop       ;just in case
    
LED0                        
; Turns on D0 LED
        bsf     STATUS, RP0     ; Bank 1
        movlw   B'00001111'     ; move predefined value to TRISIO
        movwf   TRISIO
        bcf     STATUS, RP0     ; Bank 0
        movlw   B'00010000'     ; move predefined value to GPIO
        movwf   GPIO
        goto    Main_Loop       ; go back to main loop

LED1
; Turns on D1 LED
        bsf     STATUS, RP0     ; Bank 1
        movlw   B'00001111'     ; move predefined value to TRISIO
        movwf   TRISIO
        bcf     STATUS, RP0     ; Bank 0
        movlw   B'00100000'     ; move predefined value to GPIO
        movwf   GPIO
        goto    Main_Loop       ; go back to main loop
        
LED2
; Turns on D2 LED
        bsf     STATUS, RP0     ; Bank 1
        movlw   B'00101011'     ; move predefined value to TRISIO
        movwf   TRISIO
        bcf     STATUS, RP0     ; Bank 0
        movlw   B'00010000'     ; move predefined value to GPIO
        movwf   GPIO
        goto    Main_Loop       ; go back to main loop

LED3
; Turns on D3 LED
        bsf     STATUS, RP0     ; Bank 1
        movlw   B'00101011'     ; move predefined value to TRISIO
        movwf   TRISIO
        bcf     STATUS, RP0     ; Bank 0
        movlw   B'00000100'     ; move predefined value to GPIO
        movwf   GPIO
        goto    Main_Loop       ; go back to main loop

LED4
; Turns on D4 LED
        bsf     STATUS, RP0     ; Bank 1
        movlw   B'00011011'     ; move predefined value to TRISIO
        movwf   TRISIO
        bcf     STATUS, RP0     ; Bank 0
        movlw   B'00100000'     ; move predefined value to GPIO
        movwf   GPIO
        goto    Main_Loop       ; go back to main loop

LED5
; Turns on D5 LED
        bsf     STATUS, RP0     ; Bank 1
        movlw   B'00011011'     ; move predefined value to TRISIO
        movwf   TRISIO
        bcf     STATUS, RP0     ; Bank 0
        movlw   B'00000100'     ; move predefined value to GPIO
        movwf   GPIO
        goto    Main_Loop       ; go back to main loop
    
LED6
; Turns on D6 LED
        bsf     STATUS, RP0     ; Bank 1
        movlw   B'00111001'     ; move predefined value to TRISIO
        movwf   TRISIO
        bcf     STATUS, RP0     ; Bank 0
        movlw   B'00000100'     ; move predefined value to GPIO
        movwf   GPIO
        goto    Main_Loop       ; go back to main loop
    
LED7
; Turns on D7 LED
        bsf     STATUS, RP0     ; Bank 1
        movlw   B'00111001'     ; move predefined value to TRISIO
        movwf   TRISIO
        bcf     STATUS, RP0     ; Bank 0
        movlw   B'00000010'         ; move predefined value to GPIO
        movwf   GPIO
        goto    Main_Loop       ; go back to main loop

        end