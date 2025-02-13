.data
zmienna db  "Mamma mia"
x db    40
mmia db 17 dup(5)
kys dw  3 times '?'

.code
NOP



mov ax, 04c00h
int 21h
