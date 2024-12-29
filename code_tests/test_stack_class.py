"""
This file is just a test for the stack class - it have no logical purpose, and is not necessary for
the program. It's used to test functions exposed by the Stack class
"""

from stack import Stack

ns = Stack()
sp = 2**16 - 1

ns.write(sp, 40) ; sp -= 1
ns.write(sp, 111) ; sp -= 1
ns.write(sp, 4) ; sp -= 1

def display_stack(counter = 10):
    number = 2**16 - 1
    stack = ns.read_stack()
    c2 = 0

    for i in range(counter, -1, -1):
        print(hex(number)[2:] , stack[c2])
        c2 += 1
        number -= 1

#   Display values, and add new empty line
display_stack() ; print()

#   Modify last number on the stack, by ovveriting it
sp += 1
ns.write(sp, 28) ; sp -= 1
display_stack()

#   Display last 10 values (operation not possible on normal stack - just a test of the methods)
raw_value = ns.read(2**16-10, 10) ; sp += 10
print(raw_value)