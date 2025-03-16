
# INTEGER DIVISION
## Description
This function performs division operation, while keeping sign of operation.
First, function converts numbers to their's two's compliment equivalents if
they are negative. Then typical division (as with DIV operation) is performed.
At the end, if signs of numbers are not equal, two's compliment of the result
is calculated, and stored inside AX or DX:AX. Other information are the same
as in DIV instruction. Function doesn't modify any flags.

## Summary
### Case 1 - division with 8 bit number
DIV byte 10 (for AX = 147) -> AH = 7 (00000111), AL = 14 (00001110)
### Case 2 - division with 16 bit number
DIV word 10 (for DX:AX = 147) -> DX = 7 (0000000000000111), AX = 14 (0000000000001110)
