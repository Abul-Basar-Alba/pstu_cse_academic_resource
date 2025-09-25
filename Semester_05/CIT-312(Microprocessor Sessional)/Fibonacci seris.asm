ORG 100h  ;ORG = Origin
          ;It tells the assembler where to start placing the code in memory.  
          ; 100h
          ;In DOS .COM programs, the first 256 bytes (0x0000 to 0x00FF) are reserved for the Program Segment Prefix (PSP).
          ;The actual program code starts after PSP, at offset 0x100.

MOV CX, 10          ; number of Fibonacci terms to print
MOV AX, 0           ; F(0)
MOV BX, 1           ; F(1)

PRINT_FIBO:
    ; Print the number in AX
    PUSH CX          ; save CX because printDecimal uses CX
    PUSH AX          ; save AX because printDecimal alters it

    CALL printDecimal ; print AX decimal value

    ; Print a space
    MOV DL, ' '
    MOV AH, 2
    INT 21h

    POP AX           ; restore AX
    POP CX           ; restore CX

    ADD AX, BX       ; next fib number = AX + BX
    XCHG AX, BX      ; swap AX and BX

    LOOP PRINT_FIBO

HLT  ;halts the CPU

; ------------------------------------------------------------
; Subroutine to print decimal number in AX
; Prints 0-65535 numbers to screen via DOS INT 21h, AH=2 (char output)
; Uses CX and stack, no strings used.
; ------------------------------------------------------------
printDecimal:
    PUSH DX
    PUSH BX
    MOV BX, 10
    XOR CX, CX       ; digit count
    cmp AX, 0        ;cmp AX, 0 compare this and if A!=0 then go to convertLoop
    jne convertLoop
    ; Special case for 0
    MOV DL, '0'
    MOV AH, 2
    INT 21h
    JMP donePrint 
    
    ;'0' (ASCII 48h) is stored into DL.

    ;AH=2 tells DOS to use the "character print" function.

    ;INT 21h ? DOS takes the character from DL and prints it on the screen.

convertLoop:
    XOR DX, DX       ; clear DX high for div  
                     ;Therefore, if you XOR any number with itself, all bits become zero.
                     ;Result: DX = 0
    DIV BX           ; AX / 10 quotient in AX, remainder in DX
    PUSH DX          ; store remainder (digit)
    INC CX           ;  increment
    CMP AX, 0
    JNE convertLoop

printLoop:
    POP DX
    ADD DL, '0'      ; convert digit to ASCII
    MOV AH, 2
    INT 21h
    LOOP printLoop
    
   ; The numeric digit is in DL (0–9).
   ;To print it as an ASCII character, you need to add '0' (decimal 48).
   ;Example: digit = 3 ? ASCII = 3 + 48 = 51 ? '3'

donePrint:
    POP BX
    POP DX
    RET     ;Returns control
