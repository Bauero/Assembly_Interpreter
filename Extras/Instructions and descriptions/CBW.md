
# CONVERT BYTE WORD
## Description
Extends bit on position 7 in AL to AH, by taking it's value and filling each
bit of AH with that value. Content of AL remains unchanged. Doesn't affect flags.

## EX:
- AL = 01101010 -> AL [0] == 0 -> AX = 0000000001101010
- AL = 10011101 -> AL [0] == 1 -> AX = 1111111110011101
