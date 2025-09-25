                                           ORG 100h

MOV DX, OFFSET MSG
MOV AH, 09h
INT 21h

HLT

MSG DB 'HELLO EMU8086$', 0
