; This file contains all push / pop instructinos in action. It test if everything works
; as expected.

ORG 100h

pushf

mov AX, 10
mov BX, 30
mov CX, 0
mov DX, -1

push AX
push BX
push CX
push DX

XOR AX, AX
XOR BX, BX
XOR CX, CX
XOR DX, DX

pop AX
pop BX
pop CX
pop DX

popf

XOR AX, AX
XOR BX, BX
XOR CX, CX
XOR DX, DX

mov AX, 1
mov BX, 10h
mov CX, 0101010b
mov DX, 3

pusha

XOR AX, AX
XOR BX, BX
XOR CX, CX
XOR DX, DX

popa

mov ax, 04c00h
int 21h