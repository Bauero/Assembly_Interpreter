
# ADC
## Description
This function works like ADD but after initial addition of two numbers, to 
the destination value of CF is added. This influences flags OF, SF, ZF, AF, PF, CF.

## Summary
Arg1 += Arg2
Arg1 += CF

## EX.
- ADC AX, 10 (for AX == 27, CF = 1) -> AX += 11 (00100110)
