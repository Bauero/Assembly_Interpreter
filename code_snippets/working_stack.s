ORG 100H

XOR AX,AX
XOR BX,BX
XOR CX,CX
XOR DX,DX

MOV AX, 258
MOV BX, 1032
MOV CX, 8224
MOV DX, 16512

PUSH AX
PUSH BX
PUSH CX
PUSH DX

XOR AX,AX
XOR BX,BX
XOR CX,CX
XOR DX,DX

POP DX
POP CX
POP BX
POP AX

mov ax, 04c00h
int 21h