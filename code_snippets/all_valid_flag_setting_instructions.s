; This file contains all instructins responsible for setting flags

ORG 100h

PUSHF

; Carry Flag
CLC     ; Clear
STC     ; Set
CMC     ; Reverse value
STC     ; Set
CLC     ; Clear

; Direction Flag
CLD     ; Clear
STD     ; Set
CLD     ; Clear

; Intrrupt Flag
CLI     ; Clear
STI     ; Set
CLI     ; Clear

POPF

mov ax, 04c00h
int 21h