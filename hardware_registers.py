"""
This file initializes hardware registes, along with methods for it's initializaiton
"""

from datatypes import Node
from errors import RegisterNotImplemented

class HardwareRegisters():
        
    def __init__(self):
        self._EAX = [Node(0) for _ in range(32)]
        self._AX, self._AH, self._AL = self._EAX[16:], self._EAX[16:24], self._EAX[24:]
        self._EBX = [Node(0) for _ in range(32)]
        self._BX, self._BH, self._BL = self._EBX[16:], self._EBX[16:24], self._EBX[24:]
        self._ECX = [Node(0) for _ in range(32)]
        self._CX, self._CH, self._CL = self._ECX[16:], self._ECX[16:24], self._ECX[24:]
        self._EDX = [Node(0) for _ in range(32)]
        self._DX, self._DH, self._DL = self._EDX[16:], self._EDX[16:24], self._EDX[24:]

        self.ESI = [Node(0) for _ in range(32)]
        self.EDI = [Node(0) for _ in range(32)]
        self.ESP = [Node(0) for _ in range(32)]
        self.EBP = [Node(0) for _ in range(32)]

        self._listOfRegisters = {
            "EAX" : self._EAX, "AX"  : self._AX,  "AH"  : self._AH,  "AL"  : self._AL,
            "EBX" : self._EBX, "BX"  : self._BX,  "BH"  : self._BH,  "BL"  : self._BL,
            "ECX" : self._ECX, "CX"  : self._CX,  "CH"  : self._CH,  "CL"  : self._CL,
            "EDX" : self._EDX, "DX"  : self._DX,  "DH"  : self._DH,  "DL"  : self._DL,

            "ESI" : self.ESI, "ESP" : self.ESP, "EBP" : self.EBP, "EDI" : self.EDI, 
        }

        self._regList = list(self._listOfRegisters.keys())

        self.cleanAllRegisters()

    #	inputs the restult into register r, bit by bit
    def writeIntoRegister(self, r, resutl):
        #	converstion of the number to list of binary (in str)
        listaDoWpisania = []
        if len(self._listOfRegisters[r]) == 16:
            listaDoWpisania = list("{0:016b}".format(resutl))
        elif len(self._listOfRegisters[r]) == 8:
            listaDoWpisania = list("{0:08b}".format(resutl))
        else:
            listaDoWpisania = list("{0:0b}".format(resutl))

        #	update of the register (using int, not string)
        for i in range(-1,-len(listaDoWpisania)-1,-1):
            self._listOfRegisters[r][i].data = int(listaDoWpisania[i])	

    #	return value from the register as a string of bits
    def readFromRegister(self, r):
        result = ""
        for i in self._listOfRegisters[r]: 
            result += i.printStr()
        return result

    #	if register is capable of holding effective address
    def effectiveAddressable(self, reg : str):
        if reg not in self._regList:
            raise RegisterNotImplemented
        
        effReg = ["ESI","EDI","EBP","EBX"]

        return reg in effReg

    def cleanRegister(self, r):
        # this is equal to xor(ax,ax) - or any other register
        self.writeIntoRegister(r,0)

    def cleanAllRegisters(self):
        for regiser in self._regList:
            self.cleanRegister(regiser)

    #	print the value of the registers bitly
    def printRegisters(self):

        # Filter out names shorter than 3 - ex. AX, AL etc.
        for register in filter(lambda x: len(x)==3, self._regList):
            v = self.readFromRegister(register)
            print(f"{register} : {v} = {int('0b'+v,2)}")

    def listRegisters(self):    return self._regList