ORG 100h

MOV BX, 1          ; Initial guess

SqrtLoop:
    MOV AX, BX     ; Set AX = BX before multiplication
    MUL BX         ; AX = BX * BX
    CMP AX, 25
    JG Done
    INC BX
    JMP SqrtLoop

Done:
    DEC BX         ; BX now holds sqrt

    MOV AX, BX     ; Move result to AX for printing
    CALL printDecimal

    ; Print newline (CR LF)
    MOV DL, 13
    MOV AH, 2
    INT 21h
    MOV DL, 10
    MOV AH, 2
    INT 21h

HLT

; Subroutine: print decimal number in AX
printDecimal:
    PUSH DX
    PUSH BX
    MOV BX, 10
    XOR CX, CX       ; digit counter

    CMP AX, 0
    JNE convLoop
    ; If number == 0 print '0'
    MOV DL, '0'
    MOV AH, 2
    INT 21h
    JMP donePrint

convLoop:
    XOR DX, DX
    DIV BX           ; Divide AX by 10
    PUSH DX          ; Store remainder (digit)
    INC CX
    CMP AX, 0
    JNE convLoop

printLoop:
    POP DX
    ADD DL, '0'      ; Convert digit to ASCII
    MOV AH, 2
    INT 21h
    LOOP printLoop

donePrint:
    POP BX
    POP DX
    RET
