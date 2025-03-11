;______________________________________________________________________________;
; EN                                                                           ;
; The goal of this program is to allow user to input valid equation and see it ;
; noted in RPN (Reverse Polish Notatnio)                                       ;
; EX:   '2*(8-3)-3*2+10'   ->   '2 8 3 - * 2 3 * - 10 +'                       ;
; Date: 23.02.2025                                                              ;
; Author:  Piotr Bauer                                                         ;
;_______________________________________________________________________________

org 100h
    
    ;I'm making copy of registers, and put '(' on stack (this value will be used
    ;to determine end of equation)
    push bp    
    push ax
    push bx
    push cx
    push dx
    push si
    push di
    push word 40

    call newLine

    ; Input equation and store it in variable provided from user
    readInput:
        mov ah, 10
        mov dx, instr
        int 21h

    ; Filter data
    call validEq

;#################
;    PREPARATION
;#################

    ;potrzebuję dwa wskazniki - jeden do wpisanych danych (bx)
    ; I need two pointers one to written data (bx), second to place where I want
    ; to store value
    mov bx,instr+2
    mov bp,total+2

    ; by convention, each digit ends with space - I add on one at the end of equaiton
    mov word [bp],32
    inc bp

    ; Read how long is the inputed string
    mov cx,[instr+1]
    xor ch,ch

    ; Check nesting value - each paranthesis is one level up
    mov di,level

    ;ah:
    ; copy of number during operation and keeping information that number is float not int
    ;al:
    ; information about level of last operation (0 = theres is nothing left on stack)
    mov ax,0

    ;Weight table
    ;^ = 4
    ;* = 3
    ;/ = 3
    ;+ = 2
    ;- = 2

;#################
;    TRANSLATION TO RPN
;#################

    petla:
        ;input new value to DX
        mov dx,[bx]
        xor dh,dh
        
        ;is char > 57 - if so, this can only be a '^'
        ;cmp dl,57
        ;jg if_is_power

        ;if char is < 48, meaing it's not digit but probably + - / *
        cmp dl,48
        jl equation

        ;does digit have dots - meaning it's float
        cmp ah,1
        je notSpace
        
        ;do I have to put space
        mov si, inputNum
        cmp word [si],1
        je space
        jmp notSpace

        space:
        mov word [bp],32
        inc bp
        mov word [si],0    ;bring back the flag

        notSpace:
        
        mov [bp],dl
        inc bp
        jmp repeat

        ;choose strategy
        equation:
            mov ah,0    ;clear dot/number flag

            cmp dl,40        ; (
            je open_par
            cmp dl,41        ; )
            je close_par
            cmp dl,44        ; ,
            je comma
            cmp dl,46        ; .
            je dot

            ;if this is an equation, it means we have to put space inbetween
            mov si,inputNum
            mov word [si],1

            cmp dl,47        ; /
            je division
            cmp dl,45        ; -
            je substraction
            cmp dl,43        ; +
            je addition
            cmp dl,42        ; *
            je multiplication
            
            jmp repeat

        division:
            ;make decistion depending on what is on the stack
            cmp al,3
            jge drop_div
            jmp end_div

            ; copy value from dl to ah, remove number and leave '(' on stack
            drop_div:
                mov ah,dl   
                call clear_stack
                xor dx,dx
                mov dl,ah
                push word 40

            ; put new equation on stack and set al
            end_div:
                push dx
                mov al,3
                jmp repeat

        substraction:
            ;make decistion depending on what is on the stack
            cmp al,2
            jge drop_sub
            jmp end_sub

            ; copy value from dl to ah, remove number and leave '(' on stack
            drop_sub:
                mov ah,dl   
                call clear_stack
                xor dx,dx
                mov dl,ah
                push word 40

            ; put new equation on stack and set al
            end_sub:
                push dx
                mov al,2
                jmp repeat

        addition:
            ;make decistion depending on what is on the stack
            cmp al,2
            jge drop_add
            jmp end_add

            ; copy value from dl to ah, remove number and leave '(' on stack
            drop_add:
                mov ah,dl   
                call clear_stack
                xor dx,dx
                mov dl,ah
                push word 40

            ; put new equation on stack and set al
            end_add:
            push dx
            mov al,2
            jmp repeat

        multiplication:
            ;make decistion depending on what is on the stack
            cmp al,3
            jge mnoz_zruc
            jmp mnoz_koniec

            ; copy value from dl to ah, remove number and leave '(' on stack
            mnoz_zruc:
                mov ah,dl   
                call clear_stack
                xor dx,dx
                mov dl,ah
                push word 40

            ; put new equation on stack and set al
            mnoz_koniec:
                push dx
                mov al,3
                jmp repeat

        dot:
            mov ah,1
            mov [bp],dl
            inc bp
            jmp repeat

        comma:
            mov ah,1
            mov dl,46
            mov [bp],dl
            inc bp
            jmp repeat

        open_par:
            push dx         ;put opening paranthesis on stack
            mov al,0        ;in new parantehsis there is new equation - clear al
            inc byte [di]   ;increase nesting level
            jmp repeat

        close_par:
            dec byte [di]       ;decrease nesting level
            call clear_stack    ;clear stack
            cmp byte [di],0     ;does nesting level = 0?
            je repeat

            ;If nesting level is not 0, I set al according to the last operation
            ;on the stack
            mov si,sp
            mov si,[si]          ; replace address with content stores in the address
            cmp si,47            ; /
            je last_div_mul
            cmp si,45            ; -
            je last_sub_add
            cmp si,43            ; +
            je last_sub_add
            cmp si,42            ; *
            je last_div_mul
            
            last_div_mul:
                mov al,3
                jmp repeat

            last_sub_add:
                mov al,2
                jmp repeat

        repeat:
            inc bx      ;check next equation sign
            dec cl      ;decrease value of loop
            cmp cl,0    ;if there are more chars to analyze, continue loop
            jg petla

    
    ;remove remaining equation from stack
    call clear_stack

;#################
;    VALUE CALCULATIOIN
;#################

    mov di,0            ;clear nesting level

    calculation:
        mov si,total+1
        mov ax,[si]
        add si,ax        ;now bp points to last element of equation

        ;now, we reserve place on stack for actions and digits
        sub sp,2
        mov bp,sp    ;bp points to place where we put digits on stack
        sub sp,20
        mov bx,sp    ;bx points to where we put 

        mov ax,0    ;ax wskazuje ilość liczby które mam już do dzialania


    ;Wyświetlenie wynku
    call newLine
    mov ah,9
    mov dx,total+2
    int 21h

    koniec:
    ;czyszczenie stosu
    pop di
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    pop bp

    ;zakonczenie dzialania programu
    mov ax,4c00h
    int 21h


;#################
;    DEFINICJE
;#################


;taktyczny enter
newLine:
    mov ah,2
    mov dl,10
    int 21h
ret

;clear  stosu do natrafienia na "("
clear_stack:
    pop dx
    clear:
        mov si,sp
        cmp word [si],40
        je nieczysc
        mov si,[si]
        mov word [bp],si
        inc bp
        add sp,2
        jmp clear
    nieczysc:
    add sp,2
    push dx
ret

validEq:
    mov bp,instr+1
    mov cx,[bp]    ;wczytanie ilosci wpisanych znakow
    xor ch,ch
    inc bp
    xor ax,ax
    xor dx,dx
    mov al,1

    check:
        mov dx,[bp]
        xor dh,dh

        cmp dl,40
        je nawotw
        cmp dl,41
        je nawzam

        jmp nowespr

        nawotw:
        add al,1
        jmp gzero

        nawzam:
        sub al,1

        gzero:
        cmp al,0
        jg nowespr
        mov cx,0

        nowespr:
        inc bp
        loop check

    cmp al,1
    je good

    call newLine
    mov ah,9
    mov dx,badParanthesis
    int 21h
    call newLine
    add sp,2
    xor ax,ax
    xor bp,bp
    xor cx,cx
    jmp readInput

    ;kod wykona sie jesli good wpisalem equation
    good:
        xor ax,ax
        xor bx,bx
        xor bp,bp
        xor cx,cx
ret

areNumbers:
    mov bp,instr+1
    mov cx,[bp]    ;wczytanie ilosci wpisanych znakow
    xor ch,ch
    inc bp
    mov ax,0

    searchNumbers:
        mov dx,[bp]
        xor dh,dh

        cmp dl,48
        jb noweszukanie

        cmp dl,57
        ja noweszukanie

        mov al,1
        mov cx,0

        noweszukanie:
        inc bp
        loop searchNumbers

    cmp al,1
    je weHaveNumbers

    call newLine
    mov ah,2
    mov dx,noNumbers
    int 21h
    call newLine
    add sp,2
    jmp readInput

    ;kod wykona sie jesli good wpisalem equation
    weHaveNumbers:
        xor ax,ax
        xor bx,bx
        xor bp,bp
        xor cx,cx
ret

;#################
;    VARIABLES
;#################

.DATA

;equation wpisywane przez uzytkownika
instr dw 25
      dw 0
      times 26 dw "$"
      
;total dzialania naszego programu
total dw 30
      dw 0
      times 31 dw "$"

;przechowywanie levelu zagniezdzenia nawiasow
level db 0

;przechowywanie flagi wpisywanie liczby
inputNum db 0

;estetyczne "rowna sie"
equalSign dw " = $"

;zmienna przechowujaca total naszego dzialania
sum dw 0

;zmienna przechowywujaca dlugosc ostatniej wpisaywanje liczby
numLen dw 0

;###############
;    ERROR MESSAGES
;###############

badParanthesis  dw "Paranthesis doesnt' match - correct them!$"
noNumbers       dw "There are no numbers your equation$"
zeroDivision    dw "This equaiton containt divisioin by 0 - invalid operation$"
equationError   dw "Equaiton contains logical error - ex. '+' without number$"