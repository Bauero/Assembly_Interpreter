# A single node of a singly linked list
class Node:
    
    def __init__(self, data = 0): 
        self.data = data

    def printInt(self) -> int:
        return int(self.data)
    
    def printStr(self) -> str:
        return str(self.data)
    
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
