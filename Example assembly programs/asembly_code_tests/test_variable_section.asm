; This file shows all possible approach to store data

.data
var1@ db  "Mamma mia"
x db    40
kys 3 times dw '?'

.code

mov ax, 04c00h
int 21h