
# ROTATE RIGHT
## Description
Rotates bits of number as on carousel, storing value of last moved bit in CF,
and setting OF if after rotation bit on the first place is different than before
rotation. Sets only CF and OF.

## Summary
Shift bit right, but instead of filling with 0 on the right, fill with value which
was LSB before shift

EX.
- ROR AL, CL (AL = 10110001, CL = 3):
1. 11011000 CL = 1  OF = 0
2. 01101100 CL = 0  OF = 1
3. 00110110 CL = 0  OF = 0
- ROR AL, 1 (AL = 10101101):
1. 11010110 CL = 1  OF = 0
