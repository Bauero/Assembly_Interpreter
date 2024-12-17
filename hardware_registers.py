"""
This file initializes hardware registes, along with methods for it's initializaiton
"""

from datatypes import Node
from errors import RegisterNotImplemented

class HardwareRegisters():
        
    def __init__(self):
        self._AX = [Node(0) for _ in range(16)]
        self._AH, self._AL = self._AX[-16:-8], self._AX[-8:]
        self._BX = [Node(0) for _ in range(16)]
        self._BH, self._BL = self._BX[-16:-8], self._BX[-8:]
        self._CX = [Node(0) for _ in range(16)]
        self._CH, self._CL = self._CX[-16:-8], self._CX[-8:]
        self._DX = [Node(0) for _ in range(16)]
        self._DH, self._DL = self._DX[-16:-8], self._DX[-8:]

        self._SI = [Node(0) for _ in range(16)]
        self._DI = [Node(0) for _ in range(16)]
        self._SP = [Node(0) for _ in range(16)]
        self._BP = [Node(0) for _ in range(16)]

        self._listOfRegisters = {
            "AX"  : self._AX,  "AH"  : self._AH,  "AL"  : self._AL,
            "BX"  : self._BX,  "BH"  : self._BH,  "BL"  : self._BL,
            "CX"  : self._CX,  "CH"  : self._CH,  "CL"  : self._CL,
            "DX"  : self._DX,  "DH"  : self._DH,  "DL"  : self._DL,

            "SI" : self._SI, "SP" : self._SP, "BP" : self._BP, "DI" : self._DI, 
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
        
        effReg = ["SI", "DI", "BP", "BX"]

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

    def getSize(self, register : str):
        last_letter = register.upper()[-1]
        match last_letter:
            case "X":   return 16
            case "I":   return 16
            case "P":   return 16
            case "H":   return 8
            case "L":   return 8
