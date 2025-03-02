This function perfoms jump to the speciphied location if value in CX>0;

1. Substract 1 from CX
2. Compare if CX > 0
3. If so, jump to label; if not, continue

IMPORTANT:
`... where statementLabel is the label of a statement that is a short displacement (128 bytes backward or 
127 bytes forward) from the loop instruction.`
- Introduction to 80x86 Assembly Language and Computer Architecture
- Chapter: 5.4 for Loops in Assembly Language
- ISBN 0-7637-1773-8

IMPLEMENTATION:
- Label points to instruction which is outside those boundaries, jump won't be
executed, and value in CX won't change
