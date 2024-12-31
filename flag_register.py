"""
This module define class representing flag register - it allows to perform read and 
write operations to flag register, and holds definions for meaning of each flag
"""

from extration_of_data import bitsToInt

list_of_flags = ["MD", "NT", "IO"," PL", "OF", "DF", "IF", "TF", "SF", "ZF", "PF", "CF"]

class FlagRegister():
    
	def __init__(self):
		#	initialization of a clear register
		self.FLAGS = [0 for _ in range(16)]
		self.clearFlags()

	#	set given flag to setValue
	def setFlag(self, flag, setValue):
		setValue = int(bool(setValue))
		match(flag):
			case "MD":	self.FLAGS[-16] = setValue
			case "NT":  self.FLAGS[-15] = setValue
			case "IO":  self.FLAGS[-14] = setValue
			case "PL":  self.FLAGS[-13] = setValue
			case "OF":  self.FLAGS[-12] = setValue
			case "DF":  self.FLAGS[-11] = setValue
			case "IF":  self.FLAGS[-10] = setValue
			case "TF":  self.FLAGS[-9 ] = setValue
			case "SF":  self.FLAGS[-8 ] = setValue
			case "ZF":	self.FLAGS[-7 ] = setValue
			case "AF":  self.FLAGS[-5 ] = setValue
			case "PF":  self.FLAGS[-3 ] = setValue
			case "CF":  self.FLAGS[-1 ] = setValue

	def setFlagRaw(self, valueInBits):

		if type(valueInBits) == list:
			valueInBits = "".join(valueInBits)

		if valueInBits.startswith("Ob"):
			valueInBits = valueInBits[2:]
		
		for bit in range(len(valueInBits)):
			self.FLAGS[bit] = int(valueInBits[bit] == '1')

	def setFlags(self, flagON : list = [], argOFF :list = []):
		for f in flagON: self.setFlag(f,1)
		for f in argOFF: self.setFlag(f,0)

	#	resetting self.flags
	def clearFlags(self):
		for N in range(16): self.FLAGS[N] = 0
		self.setFlag("NT",1)
		self.setFlag("IO",1)
		self.setFlag("PL",1)
		self.setFlag("IF",1)
		self.setFlag(-2,1)

	def readFlags(self) -> str:
		result = ""
		for i in self.FLAGS: result += str(i)
		return result
	
	def readFlag(self, flag : str):
		flag = flag.upper()
		if flag in list_of_flags:
			match(flag):
				case "MD":	return self.FLAGS[-16]
				case "NT":  return self.FLAGS[-15]
				case "IO":  return self.FLAGS[-14]
				case "PL":  return self.FLAGS[-13]
				case "OF":  return self.FLAGS[-12]
				case "DF":  return self.FLAGS[-11]
				case "IF":  return self.FLAGS[-10]
				case "TF":  return self.FLAGS[-9 ]
				case "SF":  return self.FLAGS[-8 ]
				case "ZF":	return self.FLAGS[-7 ]
				case "AF":  return self.FLAGS[-5 ]
				case "PF":  return self.FLAGS[-3 ]
				case "CF":  return self.FLAGS[-1 ]

	###################		CONSOLE, SHOW FLAG REGISTER CONTENT		###################		


	#	prints flag register
	def printFlags(self):
		result = self.readFlags()
		dec = bitsToInt(result)
		print(f"FL :  {result}  =  {dec}")

	#	print flag register specifically
	# 	source: https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
	def printFlagsSpec(self):
		print("Power	Sign 	Fl. Name	  Set	Meaning\n")
		print(f"15	MD	Mode Flag	  {self.FLAGS[0]}	1 NATIVE MODE |" + 
		" 0 - EMULAITON MODE (Always 1 on 8086/186, 0 on 286 and later)")
		print(f"14	NT	Nested Task FL	  {self.FLAGS[1]}	(Always 1 on 8086/186, 0 on"
		+ " 286 and later)")
		print(f"13	IO	Mode Flag	  {self.FLAGS[2]}	(Always 1 on 8086/186, 0 on 286"
		+ " and later)")
		print(f"12	PL	Mode Flag	  {self.FLAGS[3]}	(Always 1 on 8086/186, 0 on 286"
		+ " and later)")
		
		print(f"11	OF	Overflow Flag	  {self.FLAGS[4]}	1 = OV(Overflow) | 0 = NV"
		+ " (Not Overflow)")
		print(f"10	DF	Direction flag	  {self.FLAGS[5]}	1 = DN(Down) | 0 = UP(Up)")
		print(f"9	IF	Interrupt flag	  {self.FLAGS[6]}	1 = EI(Enable Interrupt) | "
		+ "0 = DI(Disable Interrupt)")
		print(f"8	TF	Trap flag 	  {self.FLAGS[7]}	-")

		print(f"7	SF	Sign flag 	  {self.FLAGS[8]}	1 = NG(Negative) | 0 = PL(Positive)")
		print(f"6	ZF	Zero flag	  {self.FLAGS[9]}	1 = NG(Negative) | 0 = PL(Positive)")
		print(f"5	-	Reserved 	  {self.FLAGS[10]}	0 - Always")
		print(f"4	AF	Auxiliary Carry	  {self.FLAGS[11]}	1 = AC(Auxiliary Carry) | 0 "
		+ "= NA(No Auxiliary Carry)")
		
		print(f"3	-	Reserved	  {self.FLAGS[12]}	0 - Always")
		print(f"2	PF	Parity Flag	  {self.FLAGS[13]}	1 = PE(Parity Even) | 0 = PO(Parity Odd)")
		print(f"1	-	Reserved	  {self.FLAGS[14]}	1 - Always")
		print(f"0	CF	Carry Flag	  {self.FLAGS[15]}	1 = CY(Carry) | 0 = NC(No Carry)")


	###################		CONSOLE, DESCRIBE FLAG REGISTER self.FLAGS		###################	

	@classmethod
	def def_overflow_flag(cls):
		"""		
		This flag is set when ther result of SIGNED operaiton is beyon the range

		EX - operation of 2 signed 8 bit intigers

		40 + 100 = 0 0100100 + 0 1100100 = 1 0001000

		We don't have enaugh space so the bit from addition OVERFLOWED the sigh flag

		Hence overflow flag is set
		"""
		return str(cls.def_overflow_flag.__doc__).replace('\t','')

	@classmethod
	def def_direction_flag(cls):
		"""
		This flag indicates in which direction strings are red

		TF = 1

		high bits -> small bits

		TF = 0

		small bits -> high bits
		"""
		return str(cls.def_direction_flag.__doc__).replace('\t','')

	@classmethod
	def def_interrupt_flag(cls):
		"""		
		If this flag is set it would allow to execute interruption caused
		by external devices (mainly to allow for smooth operation of peripherals)
		"""
		return str(cls.def_interrupt_flag.__doc__).replace('\t','')

	@classmethod
	def def_trap_flag(cls):
		"""		
		This flag indicates that processor would push to stack values of all
		registers (PUSHF & PUSHA)
		"""
		return str(cls.def_trap_flag.__doc__).replace('\t','')

	@classmethod
	def def_sign_flag(cls):
		"""		
		This flag is set depending on if we treat our number as signed of unsigned
		integer. It matters if we perform operation outside boundaries of normal number,
		because this results in operation on signed numbers instead of unsigned
		"""
		return str(cls.def_sign_flag.__doc__).replace('\t','')

	@classmethod
	def def_auxiliary_carry_flag(cls):
		"""		
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
		return str(cls.def_auxiliary_carry_flag.__doc__).replace('\t','')
	@classmethod
	def def_parity_flag(cls):
		"""		
		The sign flag defines if the number of bits in last calculated number is
		even or not

		EX:

		al = 47 -> 0010 1111 -> SF = 0 - num. of '1' in 47 is not even
		"""
		return str(cls.def_parity_flag.__doc__).replace('\t','')

	@classmethod
	def def_carry_flag(cls):
		"""		
		This flag stores result of arythmetical operations if the result (additional bit)
		couldn't fit in the register on which we perform an opperation

		EX:

		al = 255 | al + 255 (theoretically) = 510

		since that would be 111111110 => 1 11111110

		CF is set to 1 (this additional '1' from the beginning)

		al = 254 (11111110) - remaining parth that could still fit
		"""
		return str(cls.def_carry_flag.__doc__).replace('\t','')
	
	@classmethod
	def def_zero_flag(cls):
		"""
		This flag strores informaiton if the result of last arithmetical operation was
		equal to zero.
		
		"""
		return str(cls.def_zero_flag.__doc__).replace('\t','')
