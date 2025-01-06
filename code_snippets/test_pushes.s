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