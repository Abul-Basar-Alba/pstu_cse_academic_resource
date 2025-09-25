ORG 100h

MOV AX, 7
MOV BX, 6
MUL BX            ; DX:AX = AX * BX

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
; Converts CX to ASCII and prints
; ------------------------------------------------------------
printDecimal:
    PUSH AX
    PUSH BX
    PUSH DX

    MOV AX, CX
    MOV BX, 10
    XOR CX, CX           ; Digit count

    CMP AX, 0
    JNE convLoop
    MOV DL, '0'          ; Print '0' if 0
    MOV AH, 2
    INT 21h
    JMP done

convLoop:
    XOR DX, DX
    DIV BX               ; AX / 10, quotient and remainder
    PUSH DX              ; Store remainder (digit)
    INC CX
    CMP AX, 0
    JNE convLoop

printLoop:
    POP DX
    ADD DL, '0'          ; Convert to ASCII
    MOV AH, 2
    INT 21h
    LOOP printLoop

done:
    POP DX
    POP BX
    POP AX
    RET
