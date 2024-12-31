This function is responsible for writing all registers to stack. It works like this:

IMPORTANT:
`The pushad instruction pushes EAX, ECX, EDX, EBX, ESP, EBP, ESI and EDI, in this order ...
the push all and pop all instructions, including the pusha and popa instructions that push and pop the 16-bit registers.`
- Introduction to 80x86 Assembly Language and Computer Architecture
- Chapter: 5.4 for Loops in Assembly Language
- ISBN 0-7637-1773-8

-> This means, that register are pushed to the stack in the following order:

AX, CX, DX, BX, SP, BP, SI, DI - SP, contains value it had before PUSHA instruction was executed

1. Decrement SP by one - moves to next byte where content will be stored
2. Write flag register into stack
3. Decrement SP by one (2 bytes in total)