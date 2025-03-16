
# ADJUST FOR DIVISION
## Description
This function allows to prepare BCD number for division. This operation adds 
value of AH, multiplied by 10 to AL, and then sets AH to 0 (equivalent to 
XOR AH, AH). Function sets flags SF, ZF, PF according to AX value at the end 
of the operation.

## Summary:
AL = AL + AH * 10
AH = 0
