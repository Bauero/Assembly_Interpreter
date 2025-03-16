
# MULTIPLICATION
## Description
This operation performs multiplication, which internally is equivalent to 
addition of multiple values of AX or AL, each left-shifted by the offset of 
another bit from the right. This function sets flags CF and OF if upper part 
of result - DX or AH depending on operation size - is not equal to 0; otherwise 
CF and OF is set to 0. Doesn't affect other flags.

## Summary
### Case 1 - multiply by 8 bit value
`MUL byte 10` -> AX *= 10 -> if AH == 0 -> CF = 0 and OF = 0

### Case 2 - multiply by 16 bit value
`MUL word 10` -> DX:AX *= 10 -> if DX == 0 -> CF = 0 and OF = 0
