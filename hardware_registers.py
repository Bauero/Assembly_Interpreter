"""
This file initializes hardware registes, along with methods for it's initializaiton
"""

from errors import RegisterNotImplemented

class RegisterBit:
    """This class holds singular bits, which are stored in registers, this way
    it's easy to handle the same bits between whole registers and it's subparts:
    AX = AH + AL etc."""
    
    def __init__(self, data = 0): 
        self.data = data

class HardwareRegisters():
        
    def __init__(self):
        self._AX = [RegisterBit(0) for _ in range(16)]
        self._AH, self._AL = self._AX[-16:-8], self._AX[-8:]
        self._BX = [RegisterBit(0) for _ in range(16)]
        self._BH, self._BL = self._BX[-16:-8], self._BX[-8:]
        self._CX = [RegisterBit(0) for _ in range(16)]
        self._CH, self._CL = self._CX[-16:-8], self._CX[-8:]
        self._DX = [RegisterBit(0) for _ in range(16)]
        self._DH, self._DL = self._DX[-16:-8], self._DX[-8:]

        self._SI = [RegisterBit(0) for _ in range(16)]
        self._DI = [RegisterBit(0) for _ in range(16)]
        self._SP = [RegisterBit(0) for _ in range(16)]
        self._BP = [RegisterBit(0) for _ in range(16)]
        
        self._IP = [RegisterBit(0) for _ in range(16)]

        self._listOfRegisters = {
            "AX"  : self._AX,  "AH"  : self._AH,  "AL"  : self._AL,
            "BX"  : self._BX,  "BH"  : self._BH,  "BL"  : self._BL,
            "CX"  : self._CX,  "CH"  : self._CH,  "CL"  : self._CL,
            "DX"  : self._DX,  "DH"  : self._DH,  "DL"  : self._DL,

            "SI" : self._SI, "SP" : self._SP, "BP" : self._BP, "DI" : self._DI,

            "IP" : self._IP 
        }

        self._regList = list(self._listOfRegisters.keys())
        self.cleanAllRegisters()

        self.writeIntoRegister("AX", 11)
        self.writeIntoRegister("BX", 12)
        self.writeIntoRegister("CX", 13)
        self.writeIntoRegister("DX", 14)
        self.writeIntoRegister("SP", 2**16-1)
        self.writeIntoRegister("BP", 2**16-1)

    #	inputs the restult into register r, bit by bit
    def writeIntoRegister(self, r, resutl):
        r = r.upper()
        #	converstion of the number to list of binary (in str)
        listaDoWpisania = []
        if type(resutl) == int:
            if len(self._listOfRegisters[r]) == 16:
                listaDoWpisania = list("{0:016b}".format(resutl))
            elif len(self._listOfRegisters[r]) == 8:
                listaDoWpisania = list("{0:08b}".format(resutl))
            else:
                listaDoWpisania = list("{0:0b}".format(resutl))
        elif type(resutl) == list:
            listaDoWpisania = resutl

        #	update of the register (using int, not string)
        for i in range(-1,-len(listaDoWpisania)-1,-1):
            self._listOfRegisters[r][i].data = int(listaDoWpisania[i])	

    #	return value from the register as a string of bits
    def readFromRegister(self, r):
        r = r.upper()
        result = ""
        for i in self._listOfRegisters[r]: 
            result += str(i.data)
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

    def getRegisterType(self, register : str):
        register = register.upper()
        if register in self.listRegisters():
            last_letter = register[-1]
            match last_letter:
                case "X":   return "multipurpose"
                case "I":   return "index"
                case "P":   return "pointer"
                case "H":   return "multipurpose"
                case "L":   return "multipurpose"