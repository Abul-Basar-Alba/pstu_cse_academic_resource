ORG 100h

MOV AX, 1234     ; Number to convert and print
MOV CX, 0       ; Digit count

MOV BX, 10
ConvLoop:
    XOR DX, DX
    DIV BX        ; Divide AX by 10, quotient in AX, remainder in DX
    PUSH DX       ; Push remainder (digit) to stack
    INC CX
    CMP AX, 0
    JNE ConvLoop

PrintDigits:
    POP DX
    ADD DL, '0'   ; Convert digit to ASCII
    MOV AH, 02h
    INT 21h       ; DOS interrupt to print character
    LOOP PrintDigits

HLT
