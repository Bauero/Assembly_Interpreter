
# ADJUST FOR MULTIPLY
## Description
This function makes correction after multiplication of two digits in BCD code.
Internally this function divides AL by 10 and stores quotient in AH, while 
reminder is stored in AL. Function sets flags SF, ZF, PF according to AX 
value at the end of the operation.

## Summary:
AH = AL // 10
AL = AL mod 10
