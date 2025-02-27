; This file contains all valid add instructions, which should represent all possible, valid
; combinations of params which can be used with operations accepting two arguments, bounded
; by limits like, only one arg can ref. memory, and we cannot save result to immediate value
; Although ADD instructions is used, it should work with 


section .data

var1    db  10
var2    db  20

section .code

org 100H

xor ax, ax
xor bx, bx
xor cx, cx
xor dx, dx

;Register to Register:
add AX, BX
add CX, DX
add SP, BP
add SI, DI

;Immediate to Register:
add AX, 1
add BX, 1234h
add CX, 0FFh
add DX, -1
add AX, -10h
add AX, 1

MOV Bx, var2
MOV SI, var1
MOV BP, 0
MOV di, 1

;Memory to Register:
add AX, word [BX]
add BX, [SI]
add CX, [BP+DI]
add DX, [1]
add ax, 1
mov word [var1], 45

mov bx, 1

;Register to Memory:
add [BX], AX
add [SI], BX
add [BP+DI], CX
add [1], DX

;Immediate to Memory - explicite size required:
add word [BX], 1
add word [SI], 1234h
add word [BP+DI], 0FFh
add word [1], -1

add [BX], word 1
add [SI], word 1234h
add [BP+DI], word 0FFh
add [1], word -1

add [BX], byte 1
add [SI], byte 1234h
add [BP+DI], byte 0FFh      ; warning - size exceeds boundaries
add [1], byte -1

;Proper finish
mov ax, 04c00h
int 21h