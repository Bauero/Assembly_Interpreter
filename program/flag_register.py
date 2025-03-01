"""
This module define class representing flag register - it allows to perform read and 
write operations to flag register, and holds definions for meaning of each flag
"""

class FlagRegister():
    """This class simulates flag register which stores information about activation of flags,
    representing internal state of processor"""
    
    def __init__(self):
        """Initialization of ther flag register"""
        self.list_of_flags = ["MD", "NT", "IO"," PL", "OF", "DF", "IF", "TF", "SF", "ZF", "PF", "CF"]
        self.FLAGS = [0 for _ in range(16)]
        self.clearFlags()

    def setFlag(self, flag : str, setValue) -> None:
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

    def setFlagRaw(self, valueInBits : list | str) -> None:
        """This option allow to set value to all bits in flag register at once"""
        if type(valueInBits) == list:
            valueInBits = "".join(valueInBits)

        if valueInBits.startswith("Ob"):
            valueInBits = valueInBits[2:]
        
        for bit in range(len(valueInBits)):
            self.FLAGS[bit] = int(valueInBits[bit] == '1')

    def clearFlags(self) -> None:
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

    #################     CONSOLE, SHOW FLAG REGISTER CONTENT     #################

    def printFlags(self) -> str:
        result = self.readFlags()
        dec = int(result, 2)
        print(f"FL :  {result}  =  {dec}")

    def printFlagsSpec(self) -> str:
        """
        Returns description and meaning of every flag
        source: https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
        """
        description = f"""
        15	MD	Mode Flag       = {self.FLAGS[0]}   1 NATIVE MODE | 0 - EMULAITON MODE (Always 1 on 8086/186, 0 on 286 and later
        14	NT	Nested Task FL  = {self.FLAGS[1]}   (Always 1 on 8086/186, 0 on 286 and later)
        13	IO	Mode Flag       = {self.FLAGS[2]}   (Always 1 on 8086/186, 0 on 286 and later)
        12	PL	Mode Flag       = {self.FLAGS[3]}   (Always 1 on 8086/186, 0 on 286 and later)
        11	OF	Overflow Flag   = {self.FLAGS[4]}   1 = OV(Overflow) | 0 = NV" Overflow)
        10	DF	Direction flag  = {self.FLAGS[5]}   1 = DN(Down) | 0 = UP(Up)
        9	IF	Interrupt flag  = {self.FLAGS[6]}   1 = EI(Enable Interrupt) | I(Disable Interrupt)
        8	TF	Trap flag       = {self.FLAGS[7]}   
        7	SF	Sign flag       = {self.FLAGS[8]}   1 = NG(Negative) | 0 = PL(Positive)
        6	ZF	Zero flag       = {self.FLAGS[9]}   1 = NG(Negative) | 0 = PL(Positive)
        5	-	Reserved        = {self.FLAGS[10]}  0 - Always
        4	AF	Auxiliary Carry = {self.FLAGS[11]}  1 = AC(Auxiliary Carry) | 0 = NA(No Auxiliary Carry)
        3	-	Reserved        = {self.FLAGS[12]}  0 - Always
        2	PF	Parity Flag     = {self.FLAGS[13]}  1 = PE(Parity Even) | 0 = PO(Parity Odd)
        1	-	Reserved        = {self.FLAGS[14]}  1 - Always
        0	CF	Carry Flag      = {self.FLAGS[15]}  1 = CY(Carry) | 0 = NC(No Carry)
        """
        return description.replace('        ','')

    #################		CONSOLE, DESCRIBE FLAG REGISTER self.FLAGS		#################	

    @classmethod
    def def_overflow_flag(cls):
        """This function describes meaning of overflow flag"""
        description = """
        This flag is set when ther result of last operations returned result which have different sign
        than the two numbers involved in the operations if both numbers had the same sign.

        EX:
        100 (0 1100100) + 100 (0 1100100) = 200 (1 1001000) ->  0+1 => 0 -> OF=1
        -100 (1 0011100) + 120 (0 1100100) = 20 (0 0010100) ->  0+1 => 0 -> OF=0 
        """
        return description.replace('        ','')

    @classmethod
    def def_direction_flag(cls):
        """This function describes meaning of direction flag"""
        description = """
        This flag indicates in which direction strings are red

        TF = 1
        high bits -> small bits
        TF = 0
        small bits -> high bits
        """
        return description.replace('        ','')

    @classmethod
    def def_interrupt_flag(cls):
        """This function describes meaning of interrupt flag"""
        description = """		
        If this flag is set it would allow to execute interruption caused
        by external devices (mainly to allow for smooth operation of peripherals).

        This is needed for programs which have to sync, either with the user (wait for user interaction)
        or with peripherals. However, since this program doesn't allow such functionalities, usefullness
        of this flag comes down to additional bit of space which can be used. 
        """
        return description.replace('        ','')

    @classmethod
    def def_zero_flag(cls):
        """This function describes meaning of zero flag"""
        description = """
        This flag strores informaiton if the result of last arithmetical operation was
        equal to zero.
        """
        return description.replace('        ','')

    @classmethod
    def def_trap_flag(cls):
        """This function describes meaning of trap flag"""
        description = """		
        This flag indicates that processor would push to stack values of all
        registers (PUSHF & PUSHA)
        """
        return description.replace('        ','')

    @classmethod
    def def_sign_flag(cls):
        """This function describes meaning of sign flag"""
        description = """		
        This flag is set according to the sign of last arithmetic operations. It therefore
        indicated what was the value of first bit after last operaiton.
        """
        return description.replace('        ','')

    @classmethod
    def def_auxiliary_carry_flag(cls):
        """This function describes meaning of auxiliary carry flag"""
        description = """		
        This flag is set when performing addition operation on an 8-bit number, when
        there is an auxiliary bit from adding bits in the lower nibble

        EX.
        110 + 22 = 0110 1110 + 0001 0110
        11
        1110
        0110
        +____
        1 0100 - "1" on the beginning is set auxiliary flag
        """
        return description.replace('        ','')

    @classmethod
    def def_parity_flag(cls):
        """This function describes meaning of parity flag"""
        description = """		
        The sign flag defines if the number of bits in last byte of most recent calculation was
        even or not

        EX:
        al = 47 -> 0010 1111 -> SF = 0 - num. of '1' in 47 is not even
        """
        return description.replace('        ','')

    @classmethod
    def def_carry_flag(cls):
        """This function describes meaning of carry flag"""
        description = """		
        This flag stores result of arithmetical operations if the result (additional bit)
        couldn't fit in the register on which we perform an opperation

        EX:
        al = 255 | al + 255 (theoretically) = 510
        since that would be 111111110 => 1 11111110
        CF is set to 1 (this additional '1' from the beginning)
        al = 254 (11111110) - remaining parth that could still fit
        """
        return description.replace('        ','')
