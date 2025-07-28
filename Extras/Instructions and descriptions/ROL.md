
# ROTATE LEFT
## Description
Rotates bits of number as on carousel, storing value of last moved bit in CF,
and setting OF if after rotation bit on the first place is different than before
rotation. Sets only CF and OF.

## Summary
Shift bit left, but instead of filling with 0 on the right, fill with value which
was MSB before shift

## EX.
- ROL AL, CL (AL = 10010000, CL = 3):
1. 00100001 CL = 1  OF = 1
2. 01000010 CL = 0  OF = 0
3. 10000100 CL = 0  OF = 1
- ROL AL, 1 (AL = 10101101):
1. 01011011 CL = 1  OF = 1
