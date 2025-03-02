This function is responsible for writing value to stack. It works like this:

1. Decrement SP by one - moves to next byte where content will be stored
2. Write byte of data
3. If there are more bytes, go back to step 1 ; otherwise stop