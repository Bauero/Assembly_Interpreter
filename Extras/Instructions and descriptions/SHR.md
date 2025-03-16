
# SHIFT LOGICAL RIGHT
## Description
This operation shifts whole number to the right. Each shift moves least significant bit
to CF, removes most significant bit from the number, in place of the most significant
bit puts 0. Sets all flags except AF, based on the end result.

## Summary
Shift number right, putting previously LSB into CF, filling empty places with 0

## EX.
- SHR AL, 1 (AL == 255, CF = ?) -> AL = 127 (01111111), CF = 1
- SHR AL, CL (AL == 255, CL = 3, CF = ?) -> AL = 31 (00011111), CF = 1
- SHR AL, CL (AL == 100, CL = 3, CF = ?) -> AL = 12 (00001100), CF = 1
