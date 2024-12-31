This functins pops value from stack. Inside it does the following:

1. Read x bytes from the top of the stack (x, as it depends on the destinaiton)
2. Store this value in the destination
3. Incremenet value of the SP, by the amount of bytes red - this instruction
doesn't "DELETE" the data - those bits are still phisically on the stack, but they
are considered empty