XOR AX,AX
XOR BX,BX
XOR CX,CX
XOR DX,DX

;CLC
jb  jeden
jnb drugi
jmp koniec

jeden:
    ADD AX, 1
    jmp koniec

drugi:
    ADD AX, 2
    jmp koniec

koniec:
    pushf
    pop cx

mov ax, 04c00h
int 21h