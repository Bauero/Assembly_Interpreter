; This file shows all possible approach to store data

EQU ala 0

.data
instr@1897 dw 25
	  dw 0
	  times 26 dw ala
wynik dw 30
	  dw 0
	  times 31 dw "$"
var_8 db 187
var16 dw 187
var32 dd 187
var64 dq 187

.code

nop
mov ax, 04c00h
int 21h