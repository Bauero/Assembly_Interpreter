"""
This file contains stack class which represents how stack works in assembly
"""

################################################################################
#                                 CLASS ITSELF                                 #
################################################################################

import array
from errors import WrongNumberBase, IncorectValueInListOfBits
from helper_functions import *


class Stack():
    """
    This class simulates how stack in 8086 for a COM program would behave. To get more
    informaiton read literature, read sorce file or run `stack2.__doc__()` command which
    would return descripiton about funcitonality form the file.
    """

    def __init__(self):
        self.memory = array.array('b', (0 for _ in range(2**16)))
    
    def read(self, start : int, bytes : int):
        assert start >= 0, f"Tried to read stack from start = \"{start}\", which is incorrect"
        assert start <= 2**16, f"Tried to write stack from start = \"{start}\", which is incorrect"
        assert bytes > 0, f"Tried to read stack negative amount of bytes - this is not allowed"

        return self._read_raw(start, bytes)
    
    def write(self, start : int, value):
        
        assert start >= 0, f"Tried to write stack from start = \"{start}\", which is incorrect"
        assert start <= 2**16, f"Tried to write stack from start = \"{start}\", which is incorrect"
        assert type(value) in [str, int, list], "Cannort write value to stack which is in incorrect "+\
                                                "format - allowed: 'str', 'int', 'list' - value format" +\
                                                f" is {type(value)}"
        
        self._write_raw(start, covert_number_to_bit_list(value, 16))

    ############################################################################
    #   Private Methods
    ############################################################################

    def _read_raw(self, start : int, bytes : int):
        bits = []
        start -= 1 # Stack points to new address - we have to decrement it to read previous value
        for byte in range(bytes):
            # read values from memory, and append them as bits to the list
            bits.extend(list(bin(self.memory[start])[2:]))
            start -= 1
        return start, bits

    def _write_raw(self, start : int, sequence : list):

        assert len(sequence) % 8 == 0, f"Dividing sequence \"{sequence}\" to be written in stack " +\
                                        "is not dividable by 8!"
        for byte in range(len(sequence) // 8, 0, -1):
            self.memory[start] = int("".join(sequence[ 8*(byte - 1) : 8 * byte ]))
            start -= 1

        return start


def __doc__():
    definiiton = """
How Stack Works?

We assume that we will implement stack just as it would be implemented in COM application.
This kind of programm uses one segment (which is 64KB long) as place for code and stack.

This can technicly clreate hazard by allowing to ovveride the executed code by pushing values
to the stack if we make it 64KB long. However, in our example, we will not simulate this behaviour
as stack is simulated as a separate component - however, it's worth to know, that this kind of
hazard can occur if we run our code on real 16-bit machine or in emulator

Anyway, let's get to the stack. Stack will be simlated as in COM app - this means, that
addresses will be growing downwords - here is small explanation:

64KB segmet -> | 00000000 00000000 00000000 ... 00000000 00000000 00000000 |
                 ^                                                ^
            address 0h                                       address FFFFh

In our example SP and BP points to FFFFh - as one can see the only direction how the stack
can grow is by goin down - therefore if we assume:

AX = 10100100 01010101

and we perform "push AX", we would end up with those values in RAW segment:

64KB segmet -> | 00000000 00000000 00000000 ... 00000000 10100100 01010101 |
                 ^                              ^                 ^
            address 0h                SP = address FFFDh     address FFFFh

and our SP would point to FFFD (because it points to first free bajt looking from the back of the
current segment).

Therefore, push instruction works like:     write byte  -> decrement SP -> repeat if needed

And pop instruction works like:             increment SP -> read byte -> repeat if needed


Little or bit endian?

-> Values are stored using little endian.

                                                                                     {ADDRESS}  {VALUE}
So for our AX example:                                                                            ...
                                                                                        FFFD    00000000
AX = 10100100 01010101 ->       AH = 10100100 -> ADDRES: FFFEh      ->      STACK:      FFFE    10100100
                                AL = 01010101 -> ADDRES: FFFFh                          FFFF    01010101
                                                                (end of segment)  __________________________

Simplified example of how bits are pushed to the stack:

Push ASDFGHJK  ->  { segment beginning -> | ... A S D F G H J K | <- segment end }
"""
    return definiiton
