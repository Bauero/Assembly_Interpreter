
# SHIFT ARITHMETIC RIGHT
## Description
This operation shifts whole number (except most significant bit) to the right.
Least significant bit is moved to CF, while in place of second most significant
bit 0 is placed. Affects all flags except AF.

## Summary
Shift number right except most significant bit

## EX.
- SAR AL, 1 (AL == 255, CF = ?) -> AL = 191 (10111111), CF = 1
- SAR AL, CL (AL == 255, CL = 3, CF = ?) -> AL = 143 (10001111), CF = 1
- SAR AL, CL (AL == 100, CL = 3, CF = ?) -> AL = 12 (00001100), CF = 1
