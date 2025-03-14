
# SUB
## Description
This function performs binary addition of two number as A - B is equivalent
to A + B', where B' is two's compliment of B.
This influences flags OF, SF, ZF, AF, PF, CF.

## Summary
Arg1 -= Arg2

## EX.
- SUB AX, 10 (for AX == 27) -> AX -= 10 (00010001)
