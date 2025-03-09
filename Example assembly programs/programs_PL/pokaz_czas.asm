;______________________________________________________________________________;
; EN                                                                           ;
; This file's goal is to write current time in the DosBox'es console in format ;
; HH:MM:SS.MS                                                                  ;
; Date: 6.01.2025                                                              ;
; Author:  Piotr Bauer                                                         ;
;______________________________________________________________________________;


section .code

;###############################################################################
;   Main program
;###############################################################################

org 100h                ;   Offset where code is written - mandatory for .COM program
mov dx, 10              ;   write LF - line feed
call showCharDl

mov dl, 13              ;   write CR - carrige return
call showCharDl

call readTime

;   Move values to Stack
push DX
push CX

call showHighBits   ; Hour
call writeColon     ; :
call showLowBits    ; Minutes
call writeColon     ; :
add sp, 2           ; move from reading H/M to S/MS
call showHighBits   ; Seconds
call writeDot       ; .
call showLowBits    ; Miliseconds
call theEnd

;###############################################################################
;   Function used in the program
;###############################################################################

showHighBits:
    call cleanRegisters
    mov bx, sp                      ; store sp address (value) in bx
    add bx, 2                       ; make bx point to number, not return address
    mov bx, [bx]                    ; store in bx value which is poited by adderss in bx
    mov al, bh                      ; move upper bits to al, for future division
    call displayTwoDigitNumber
    ret

showLowBits:
    call cleanRegisters
    mov bx, sp
    add bx, 2
    mov bx, [bx]
    mov al, bl
    call displayTwoDigitNumber
    ret

displayTwoDigitNumber:
    mov dx, 10                      ; store divider in register
    div dl                          ; divide
    mov dl, al                      ; store value for addition
    or dl, 30h                      ; eqivalend to add dl, 30h
    call showCharDl
    mov dl, ah                      ; store reminder for display
    or dl, 30h                      ; eqivalend to add dl, 30h
    call showCharDl
    ret

cleanRegisters:
    xor ax, ax
    xor bx, bx
    xor cx, cx
    xor dx, dx
    ret

showCharDl:
    pusha
    mov ah, 2
    int 21h
    popa
    ret

readTime:
    ;   Read time and store it like this
    ;   CH: hour    CL: minutes
    ;   DH: second  DL: miliseconds
    push ax
    mov ah, 2Ch
    int 21h
    pop ax
    ret

writeColon:
    pusha
	mov ah,2
	mov dl,58
	int 21h
    popa
	ret

writeDot:
    pusha
	mov ah,2
	mov dl,46
	int 21h
    popa
	ret

theEnd:
    mov ah, 0
    int 21h
