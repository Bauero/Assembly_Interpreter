
# DECIMAL ADJUST FOR subtraction
## Description
Decimal adjust after binary subtraction in BCD code. This function performs 
the following operation. If lower nibble in AL is greater than 9 or AF is set, 
function subtracts 6 from AL, and sets AF to 1. Then function check if AL is 
greater than 9Fh (159) or if the CF is set. If any of those conditions is met, 
function subtracts 60h (96) from AL and sets CF to 1.
This function influences flags SF, ZF, AF, PF, CF.

## Summary:
0. if (AL ^ 0Fh) > 9 or AF == 1 do the following:
1. AL = AL - 6;
2. AF = 1
3. if AL > 9Fh or CF = 1
4. AL = AL - 60h
5. CF = 1

## EX:
- AL = 00000011, AF = 1 -> AL -= 6 (11111101) -> AF = 1 -> (AL > 9Fh) -> AL -= 96 (10100111) -> CF = 1
- AL = 11101011, AF = 0 -> AL -= 6 (11100101) -> AF = 1 -> (AL > 9Fh) -> AL -= 96 (10000101) -> CF = 1
- AL = 00001000, AF = 0 -> Nothing (conditions aren't met)
