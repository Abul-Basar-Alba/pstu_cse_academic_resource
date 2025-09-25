ORG 100h

MOV AX, 1234h
MOV BX, 4321h
ADD AX, BX       ; AX = AX + BX

MOV CX, AX       ; Move result to CX for printing

CALL printDecimal

; Print newline (CR LF)
MOV DL, 13
MOV AH, 02h
INT 21h
MOV DL, 10
MOV AH, 02h
INT 21h

HLT

; ------------------------------------------------------------
; Subroutine to print decimal number in CX
; Converts CX to ASCII digits and prints them using DOS INT 21h
; ------------------------------------------------------------
printDecimal:
    PUSH AX
    PUSH BX
    PUSH DX

    MOV AX, CX
    MOV BX, 10
    XOR CX, CX         ; digit count

    CMP AX, 0
    JNE convLoop
    MOV DL, '0'        ; Print '0' if number is zero
    MOV AH, 2
    INT 21h
    JMP donePrint

convLoop:
    XOR DX, DX
    DIV BX             ; AX / 10 -> quotient in AX, remainder in DX
    PUSH DX            ; store remainder (digit)
    INC CX
    CMP AX, 0
    JNE convLoop

printLoop:
    POP DX
    ADD DL, '0'        ; Convert digit to ASCII character
    MOV AH, 2
    INT 21h
    LOOP printLoop

donePrint:
    POP DX
    POP BX
    POP AX
    RET
