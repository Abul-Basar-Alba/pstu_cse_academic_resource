ORG 100h

MOV AX, 9         ; Number to convert to binary
MOV CX, 16        ; Number of bits
MOV DX, 8000h     ; Mask starting at highest bit (bit 15)

PrintBin:
    TEST AX, DX   ; Test current bit
    JZ PrintZero
    MOV DL, '1'
    JMP PrintOut

PrintZero:
    MOV DL, '0'

PrintOut:
    MOV AH, 02h   ; DOS print character
    INT 21h
    SHR DX, 1     ; Move mask to next bit
    LOOP PrintBin

; Print newline (CR LF)
MOV DL, 13
MOV AH, 02h
INT 21h
MOV DL, 10
MOV AH, 02h
INT 21h

HLT
