ORG 100h

MOV AH, 02h    ; DOS function to print a character

MOV DL, 'H'
INT 21h

MOV DL, 'e'
INT 21h

MOV DL, 'l'
INT 21h

MOV DL, 'l'
INT 21h

MOV DL, 'o'
INT 21h

MOV DL, ','
INT 21h

MOV DL, ' '
INT 21h

MOV DL, 'W'
INT 21h

MOV DL, 'o'
INT 21h

MOV DL, 'r'
INT 21h

MOV DL, 'l'
INT 21h

MOV DL, 'd'
INT 21h

MOV DL, '!'
INT 21h

; Print newline (CR + LF)
MOV DL, 13
INT 21h
MOV DL, 10
INT 21h

HLT
