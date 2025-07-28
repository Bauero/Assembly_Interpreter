
# ROTATE THROUGH CARRY LEFT
## Description
Perform rotation as if carry flag was an additional, most significant bit of number
```
CF   +f e d c b a 9 8 7 6 5 4 3 2 1 0

0+0 0 0 0 0 0 0 1 1 1 0 1 0 1 1 1
```
After one rotation bit form last position is moved into CF, previous value of CF is moved
into 'f' and each other bit is shifted one right
```
CF   +f e d c b a 9 8 7 6 5 4 3 2 1 0

1+0 0 0 0 0 0 0 0 1 1 1 0 1 0 1 1
```
## EX.
- RCL AL, 3 (AL = 00011111 , CL = 1):
1. 00111111 CL = 0  OF = 0
2. 01111110 CL = 0  OF = 0
3. 11111100 CL = 0  OF = 1
- RCL AL, 1 (AL = 10101101, CL = 0):
1. 01011010 CL = 1  OF = 1
