
# CONVERT WORD DOUBLEWORD
## Description
Extends bit on position 15 in AX to DX, by taking it's value and filling each
bit of DX with that value. Content of AX remains unchanged. Doesn't affect flags.

## EX:
- AX = 0110101010110010 -> AX [0] == 0 -> DX:AX = 0000000000000000:0110101010110010
- AX = 1001110110100111 -> AX [0] == 1 -> DX:AX = 1111111111111111:1001110110100111
