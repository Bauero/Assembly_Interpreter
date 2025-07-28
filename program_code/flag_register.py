"""
This module define class representing flag register - it allows to perform read and 
write operations to flag register, and holds definitions for meaning of each flag
"""

class FlagRegister():
    """This class simulates flag register which stores information about activation of flags,
    representing internal state of processor"""
    
    def __init__(self):
        """Initialization of the flag register"""
        self.list_of_flags = ["MD", "NT", "IO"," PL", "OF", "DF", "IF", "TF", "SF", "ZF", "PF", "CF"]
        self.FLAGS = [0 for _ in range(16)]
        self.clearFlags()

    def setFlag(self, flag : str, setValue):
        """Allow to set specific flag"""
        setValue = int(bool(int(setValue)))
        match(flag):
            case "MD":	self.FLAGS[0 ] = setValue
            case "NT":  self.FLAGS[1 ] = setValue
            case "IO":  self.FLAGS[2 ] = setValue
            case "PL":  self.FLAGS[3 ] = setValue
            case "OF":  self.FLAGS[4 ] = setValue
            case "DF":  self.FLAGS[5 ] = setValue
            case "IF":  self.FLAGS[6 ] = setValue
            case "TF":  self.FLAGS[7 ] = setValue
            case "SF":  self.FLAGS[8 ] = setValue
            case "ZF":	self.FLAGS[9 ] = setValue
            case "AF":  self.FLAGS[11] = setValue
            case "PF":  self.FLAGS[13] = setValue
            case "CF":  self.FLAGS[15] = setValue

    def setFlagRaw(self, valueInBits : list | str):
        """This option allow to set value to all bits in flag register at once"""
        if type(valueInBits) == list:
            valueInBits = "".join(valueInBits)

        if valueInBits.startswith("Ob"):
            valueInBits = valueInBits[2:]
        
        for bit in range(len(valueInBits)):
            self.FLAGS[bit] = int(valueInBits[bit] == '1')

    def clearFlags(self):
        """Set all flags to default value"""
        for N in range(16): self.FLAGS[N] = 0
        self.setFlag("NT",1)
        self.setFlag("IO",1)
        self.setFlag("PL",1)
        self.setFlag("IF",1)
        self.setFlag(-2,1)

    def readFlags(self) -> str:
        """Return value of flag register as a str"""
        result = ""
        for i in self.FLAGS: result += str(i)
        return result
    
    def readFlag(self, flag : str) -> int:
        """Return value of certain flag as int value - 0 or 1"""
        flag = flag.upper()
        if flag in self.list_of_flags:
            match(flag):
                case "MD":  return self.FLAGS[0 ]
                case "NT":  return self.FLAGS[1 ]
                case "IO":  return self.FLAGS[2 ]
                case "PL":  return self.FLAGS[3 ]
                case "OF":  return self.FLAGS[4 ]
                case "DF":  return self.FLAGS[5 ]
                case "IF":  return self.FLAGS[6 ]
                case "TF":  return self.FLAGS[7 ]
                case "SF":  return self.FLAGS[8 ]
                case "ZF":  return self.FLAGS[9 ]
                case "AF":  return self.FLAGS[11]
                case "PF":  return self.FLAGS[13]
                case "CF":  return self.FLAGS[15]
