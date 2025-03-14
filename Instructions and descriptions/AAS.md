
# ADJUST AFTER subtraction.
## Description
This function is designed to adjust score after subtraction on number stored in BCD code.

The purpose of this operation is to separate number stored in AL in binary form to 
number stored in AH and AL in BCD form. What it does, is check if number in AL is greater
than 9, or overflow to upper nibble of AL occurred (AF == 1), and if so, it subtracts one to 
from AH, subtracts 6 from AL, sets both AF to 1 and CF to 1, and clears bits of upper nibble in 
AL. This operation doesn't affect other flags.

## Summary:
If (AL ^ 0Fh) > 9 or AF == 1 do the following:
1. AL = AL - 6
2. AH = AH - 1
3. AF = 1
4. CF = 1
5. AL = AL ^ 0Fh

## EX:
- AL = 01001010, AF = 1 -> AH -= 1 -> AL -= 6 (01000100) -> CF = 1, AF = 1 -> AL = AL ^ 15 -> AL = 4  (00000100)
- AL = 10101010, AF = ? -> AH -= 1 -> AL -= 6 (10100100) -> CF = 1, AF = 1 -> AL = AL ^ 15 -> AL = 4  (00000100)
- AL = 00001000, AF = 0 -> Nothing (conditions aren't met)
