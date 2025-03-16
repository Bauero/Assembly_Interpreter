
# SUB
## Description
This function works like SUB, but it subtracts value of CF form the result
of A - B. Therefore it's equivalent to A - B - C, or A - (B + C). As in SUB
function, we use the informaiton, that A-B is equal to A-B' if B' is two's
compliment of B. Therefore SBB adds CF to B, calculates two's compliment of
this value, and then performs addition of result to A.
This influences flags OF, SF, ZF, AF, PF, CF.

## Summary
Arg1 -= Arg2
Arg1 -= CF

## EX.
- SBB AX, 10 (for AX == 27, CF = 1) -> AX -= 11 (00010000)
