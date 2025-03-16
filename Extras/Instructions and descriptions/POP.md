
# POP VALUE FROM STACK
## Description
This function pops value from stack. Inside it does the following:

1. Read x bytes from the top of the stack (x, as it depends on the destinaiton)
2. Store this value in the destination
3. Increment value of the SP, by the amount of bytes red - this instruction
doesn't "DELETE" the data - those bits are still physically on the stack

## IMPORTANT

Based on my experience with NASM, when we are POP'ing value from stack we need to store
it in any place which would accept 16 bits - if we put in memory, in place where we
store 8 bit variable, pop would return and store 16 bit, effectively overwriting any
byte which is stored in memory after the initial byte. Doing so in this simulator, if
we push to 8 bit variable which is last in our data, would probably throw an error, as
(in terms of memory) program reserves only the space which is declared by variables, while
doing so in NASM for .COM program would *probably* just override any byte which is first
in segment !
