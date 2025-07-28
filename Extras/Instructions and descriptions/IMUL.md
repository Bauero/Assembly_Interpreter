
# INTEGERS MULTIPLICATION
## Description
This operation performs multiplication but takes into account sigh of the 
numbers. First, function finds two's compliment of arguments (DX:AX or AX and
function Argument) of those values which are negative. Then, it performs normal
mutiplication. Then if signs of numbers were not equal it calculates two's 
compliment of the result. Final value is stored in AX (for 8 bit multiplication) or
DX:AX (for 16 bit multiplication). Flags CF and OF are set if upper half 
doesn't only contains bits with value of the sign of lower half. (for 8 bit, 
if AH != 00000000 if AL 0??????? or AH != 11111111 if AL 1???????).
Other flags are not changed.

## Summary
### Case 1 - multiply by 8 bit value
`IMUL byte 10` -> AX *= 10; CBW AL != current AX value, set CF = 1 and OF = 1

### Case 2 - multiply by 16 bit value
`IMUL word 10` -> DX:AX *= 10; CWD AX != current DX:AX value, set CF = 1 and OF = 1
