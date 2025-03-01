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

    def __str__(self):  return str(self.data)

class HardwareRegisters():
    """This class contains all registers which are available in the interpreter"""

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
        self.writeIntoRegister("SP", 2**16-1)
        self.writeIntoRegister("BP", 2**16-1)

    def writeIntoRegister(self, register, value):
        """This method inputs value into register bit by bit"""
        
        register = register.upper()
        listaDoWpisania = []
        if type(value) == int:
            size = len(self._listOfRegisters[register])
            listaDoWpisania = list(f"{value:0{size}b}")
        elif type(value) == list:
            listaDoWpisania = value

        for i in range(-1,-len(listaDoWpisania)-1,-1):
            self._listOfRegisters[register][i].data = int(listaDoWpisania[i])

    def readFromRegister(self, register) -> str:
        """This method returns content of the register which is passed as an argument"""
        
        register = register.upper()
        return "".join(map(str, self._listOfRegisters[register]))

    def effectiveAddressable(self, register : str) -> bool:
        """This method return True/False depending on if the register which is
        passed as an argument allow for storage and read of value from memory
        of which address is stored inside register"""
        
        register = register.upper()
        if register not in self._regList:    raise RegisterNotImplemented
        effReg = ["SI", "DI", "BP", "BX"]
        return register in effReg

    def cleanRegister(self, register : str) -> None:
        """Set value of register to 0"""

        register = register.upper()
        self.writeIntoRegister(register, 0)

    def cleanAllRegisters(self) -> None:
        """Set value of each register to 0"""

        for regiser in self._regList:   self.cleanRegister(regiser)

    def printRegisters(self):
        """Write in console value of each register"""

        # Filter out names shorter than 3 - ex. AX, AL etc.
        for register in filter(lambda x: len(x)==3, self._regList):
            v = self.readFromRegister(register)
            print(f"{register} : {v} = {int('0b'+v,2)}")

    def listRegisters(self) -> list:
        """Return list of availavle registers"""

        return self._regList

    def getSize(self, register : str) -> int:
        """Return size of register - returns -1 for unknown registers' name"""

        register = register.upper()
        last_letter = register.upper()[-1]
        match last_letter:
            case "X":   return 16
            case "I":   return 16
            case "P":   return 16
            case "H":   return 8
            case "L":   return 8
            case _:     return -1

    def getRegisterType(self, register : str) -> str:
        """Return type of register, according to it's purpose"""

        register = register.upper()
        if register in self.listRegisters():
            last_letter = register[-1]
            match last_letter:
                case "X":   return "multipurpose"
                case "I":   return "index"
                case "P":   return "pointer"
                case "H":   return "multipurpose"
                case "L":   return "multipurpose"
                case _:     return ""
