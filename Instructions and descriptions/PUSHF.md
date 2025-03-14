
# PUSH VALUE OF FLAG REGISTER TO STACK
## Description
This function is responsible for writing flag register to stack. It works like this:
1. Decrement SP by one - moves to next byte where content will be stored
2. Write flag register into stack
3. Decrement SP by one (2 bytes in total)
