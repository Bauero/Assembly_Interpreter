
# ADJUST AFTER ADDITION.
## Description
This function is designed to adjust score after addition on number stored in BCD code.
The purpose of this operation is to separate number stored in AL in binary form to 
number stored in AH and AL in BCD form. What it does, is check if number in AL is greater
than 9, or overflow to upper nibble of AL occurred (AF == 1), and if so, it adds one to 
to AH, adds 6 to AL, sets both AF to 1 and CF to 1, and clears bits of upper nibble in 
AL. This operation doesn't affect other flags.

## Summary:
If (AL ^ 0Fh) > 9 or AF == 1 do the following:
1. AL = AL + 6
2. AH = AH + 1
3. AF = 1
4. CF = 1
5. AL = AL ^ 0Fh

## EX:
- AL = 00010110, AF = 1 -> AH += 1 -> AL += 6 (00011100) -> CF = 1, AF = 1 -> AL = AL ^ 15 -> AL = 12 (00001100)
- AL = 10101010, AF = ? -> AH += 1 -> AL += 6 (10110000) -> CF = 1, AF = 1 -> AL = AL ^ 15 -> AL = 0  (00000000)
- AL = 00001000, AF = 0 -> Nothing (conditions aren't met)
