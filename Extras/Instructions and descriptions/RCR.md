
# ROTATE THROUGH CARRY RIGHT
## Description
Perform rotation as if carry flag was an additional, least significant bit of number
```
f e d c b a 9 8 7 6 5 4 3 2 1 0   +   CF

1 0 1 0 1 1 1 0 1 0 1 0 1 0 1 0   +   1
```
after one rotation bit from 'f' is moved into 'e', bit from '0' to CF, and previous value
of 'CF' is moved into 'f'
```
f e d c b a 9 8 7 6 5 4 3 2 1 0   +   CF

1 1 0 1 0 1 1 1 0 1 0 1 0 1 0 1   +   0
```
## EX.
- RCR AL, CL (AL = 00011111 , CL = 3):
1. 10001111 CL = 1  OF = 1
2. 11000111 CL = 1  OF = 0
3. 11100011 CL = 1  OF = 0
- RCL AL, 1 (AL = 11111111):
1. 01111111 CL = 1  OF = 1
