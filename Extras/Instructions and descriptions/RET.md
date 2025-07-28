Performs jump to address which is defined in 16 bit value to which SP points to.
Equivalent to (although RET doesn't change any register except SP):
```
POP AX
JMP AX
```
