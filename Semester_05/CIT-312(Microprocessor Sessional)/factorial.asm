ORG 100h

MOV CX, 5         ; Number to calculate factorial of
MOV AX, 1         ; Initialize AX to 1 for multiplication

FactLoop:
    MUL CX
    LOOP FactLoop
    ; Result in AX

MOV CX, AX        ; Move result to CX for printing

CALL printDecimal

; Print newline (CR LF)
MOV DL, 13
MOV AH, 2
INT 21h
MOV DL, 10
MOV AH, 2
INT 21h

HLT

; ------------------------------------------------------------
; Subroutine to print decimal number in CX
; Converts CX to ASCII digits and prints them via DOS INT 21h
; ------------------------------------------------------------

printDecimal:
    PUSH AX
    PUSH BX
    PUSH DX

    MOV AX, CX
    MOV BX, 10
    XOR CX, CX     ; Digit count

    CMP AX, 0
    JNE convLoop
    MOV DL, '0'    ; Print '0' if number is zero
    MOV AH, 2
    INT 21h
    JMP donePrint

convLoop:
    XOR DX, DX
    DIV BX
    PUSH DX        ; Store remainder digit
    INC CX
    CMP AX, 0
    JNE convLoop

printLoop:
    POP DX
    ADD DL, '0'
    MOV AH, 2
    INT 21h
    LOOP printLoop

donePrint:
    POP DX
    POP BX
    POP AX
    RET
