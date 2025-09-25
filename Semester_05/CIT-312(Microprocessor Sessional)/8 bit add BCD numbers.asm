ORG 100h

MOV AL, 25h    ; BCD 25
MOV BL, 37h    ; BCD 37

ADD AL, BL
DAA            ; Decimal Adjust after Addition

; Print result stored in AL as two BCD digits

MOV AH, 2      ; DOS print char

; Print tens digit
MOV DL, AL
AND DL, 0F0h    ; Get upper nibble (tens)
SHR DL, 4
ADD DL, '0'
INT 21h

; Print units digit
MOV DL, AL
AND DL, 0Fh     ; Get lower nibble (units)
ADD DL, '0'
INT 21h

HLT
