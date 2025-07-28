
# DIVISION
## Description
This function performs standard division treading both arguments as unsigned nubmers.
First argument is always AX (for division with byte-size value) or 
DX:AX (for division with word-size value). Quotient is stored in lover half, of first
argument (AL or AX) and reminder in the upper half (AH or DX). This operation doesn't 
affect any flags.

## Summary
### Case 1 - division with 8 bit number
DIV byte 10 (for AX = 147) -> AH = 7 (00000111), AL = 14 (00001110)
### Case 2 - division with 16 bit number
DIV word 10 (for DX:AX = 147) -> DX = 7 (0000000000000111), AX = 14 (0000000000001110)
