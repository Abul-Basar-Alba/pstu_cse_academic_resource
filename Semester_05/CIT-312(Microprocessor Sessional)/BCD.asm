ORG 100h

MOV AL, 42h    ; BCD 42
MOV BL, 19h    ; BCD 19

SUB AL, BL
DAA            ; Decimal Adjust after Subtract

MOV AH, 0     ; Clear AH for printing

; Convert BCD in AL to two ASCII digits and print
MOV AH, 2      ; DOS print char function

; Print tens digit
MOV DL, AL
AND DL, 0F0h   ; Mask tens digit
SHR DL, 4
ADD DL, '0'
INT 21h

; Print units digit
MOV DL, AL
AND DL, 0Fh    ; Mask units digit
ADD DL, '0'
INT 21h

HLT
