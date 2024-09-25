# A single node of a singly linked list

import numpy
from array import array

class Node:
    
    def __init__(self, data = 0): 
        self.data = data

    def printInt(self) -> int:
        return int(self.data)
    
    def printStr(self) -> str:
        return str(self.data)
    
class Register:

    def __init__(self, size = 16, value = 0):
        match size:
            case 8:     self.bits = numpy.zeros(1, numpy.int8)
            case 16:    self.bits = numpy.zeros(1, numpy.int16)
            case 32:    self.bits = numpy.zeros(1, numpy.int32)
            case _:     self.bits = numpy.zeros(1, numpy.int_)

        self.shape = (1, size)

    def str(self):      return str(self.bits)

    def repr(self):     return f"0b{self.str()}"

    


class Variable:

    __variables = 0

    def __init__(self, size,  data, name):
        self.data = data
        self.name = name
        self.size = size
        self.address = self.__variables

        #   new variable has the number one grater than the previous one
        Variable.__variables += 1

    def getSize(self):
        if self.size == "dw": return 16
        elif self.size == "byte": return 8
