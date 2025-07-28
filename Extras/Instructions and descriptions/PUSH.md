
# PUSH VALUE TO STACK
## Description
This function is responsible for writing value to stack. It works like this:

1. Decrement SP by one - moves to next byte where content will be stored
2. Write byte of data
3. If there are more bytes, go back to step 1 ; otherwise stop

## IMPORTANT

There is quite interesting behaviour implemented into NASM if we are operating
on values smaller than 16 bits - basically, value provided is stretched to fit
into 16 bits, and the stretching is done based on left-most bit:

-> If we push 8 bit value left-most bit is coppied into all places:

_ _ _ _ _ _ _ _ 1 0 0 0 0 0 0 0

1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 -> 255  128

############################################################################

_ _ _ _ _ _ _ _ 0 1 1 1 0 1 0 1

0 0 0 0 0 0 0 0 0 1 1 1 0 1 0 1 -> 000  117

## Raw example:

Val First Byte  Second Byte

- PUSH byte 127  -> 000 127
- PUSH word 127  -> 000 127
- PUSH byte 128  -> 255 128
- PUSH word 128  -> 000 128
- PUSH byte 260  -> 000 004
- PUSH word 260  -> 001 004
