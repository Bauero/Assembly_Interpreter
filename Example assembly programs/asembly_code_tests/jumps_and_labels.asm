; This code ilustrates use of jumps and 

ORG 100h

XOR BX,BX
XOR CX,CX
XOR DX,DX

;CLC
jb  first
jnb second
jmp koniec

first:
    jmp koniec

second:
    mov ax, 04c00h
    jmp koniec

koniec:
    pushf

int 21h