; Example assembly language program — adds two numbers
; Author:  R. Detmer
; Date:    revised 7/97

.386
.MODEL FLAT

ExitProcess PROTO NEAR32 stdcall, dwExitCode:DWORD
EXTRN Procedure1:NEAR32, Procedure2:NEAR32 

INCLUDE io.h            ; header file for input/output

cr      EQU     0dh     ; carriage return character
Lf      EQU     0ah     ; line feed

.STACK  4096            ; reserve 4096-byte stack

.DATA
var dq 18
number1 DWORD   ?
number2 DWORD   ?
prompt1 BYTE    "Enter first number:  ", 0
prompt2 BYTE    "Enter second number:  ", 0
string  BYTE    40 DUP (?)
label1  BYTE    cr, Lf, "The sum is "
sum     BYTE    11 DUP (?)
        BYTE    cr, Lf, 0

.CODE                           ; start of main program code
_start:
    output  prompt1         ; prompt for first number
    input   string, 40      ; read ASCII characters
    atod    string          ; convert to integer
    mov     number1, eax    ; store in memory
    
    output  prompt2         ; repeat for second number
    input   string, 40
    atod    string
    mov     number2, eax
    
    mov     eax, number1    ; first number to EAX
    add     eax, number2    ; add second number
    dtoa    sum, eax        ; convert to ASCII characters
    output  label1          ; output label and sum

    INVOKE  ExitProcess, 0  ; exit with return code 0

PUBLIC _start                   ; make entry point public END

END                             ; end of source code
