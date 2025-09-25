ORG 100h

MOV AX, 1000h
MOV BX, 200h
SUB AX, BX

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
; Converts CX to ASCII and prints using DOS INT 21h AH=2
; ------------------------------------------------------------
printDecimal:
    PUSH AX
    PUSH BX
    PUSH DX

    MOV AX, CX
    MOV BX, 10
    XOR CX, CX           ; digit counter

    CMP AX, 0
    JNE convLoop
    MOV DL, '0'          ; Print '0' if 0
    MOV AH, 2
    INT 21h
    JMP done

convLoop:
    XOR DX, DX
    DIV BX               ; AX / 10 -> AX quotient, DX remainder
    PUSH DX              ; store digit
    INC CX
    CMP AX, 0
    JNE convLoop

printLoop:
    POP DX
    ADD DL, '0'          ; Convert digit to ASCII
    MOV AH, 2
    INT 21h
    LOOP printLoop

done:
    POP DX
    POP BX
    POP AX
    RET
