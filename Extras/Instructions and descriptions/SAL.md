
# SHIFT ARITHMETIC LEFT
## Description
This operation shifts whole number to the left. Each shift moves most significant bit
to CF, removes most significant bit from the number, and at the end, as the least 
significant bit puts 0. Sets all flags except AF, based on the end result.

## Summary
Shift number left, putting previously MSB into CF, filling empty places with 0

## EX.
- SAL AL, 1 (AL == 255, CF = ?) -> AL = 254 (11111110), CF = 1
- SAL AL, CL (AL == 255, CL = 3, CF = ?) -> AL = 248 (11111000), CF = 1
- SAL AL, CL (AL == 1, CL = 3, CF = ?) -> AL = 8 (00001000), CF = 0
