"""
This module is responsible to hold all register and all operatrion needed for
it to work properly

Flag register is register which stores 16 different bits - most of which holds
information about globbal setting of the processor or the program (like parity
flga, sign flag etc.)
"""


from extration_of_data import bitsToInt

#	initialization of a clear register
FLAGS = [0 for _ in range(16)]

#	set given flag to setValue
def setFlag(flag,setValue):
	match(flag):
			case "MD":	FLAGS[-16] = setValue
			case "NT":  FLAGS[-15] = setValue
			case "IO":  FLAGS[-14] = setValue
			case "PL":  FLAGS[-13] = setValue
			case "OF":  FLAGS[-12] = setValue
			case "DF":  FLAGS[-11] = setValue
			case "IF":  FLAGS[-10] = setValue
			case "TF":  FLAGS[-9 ] = setValue
			case "SF":  FLAGS[-8 ] = setValue
			case "ZF":  FLAGS[-5 ] = setValue
			case "PF":  FLAGS[-3 ] = setValue
			case "CF":  FLAGS[-1 ] = setValue
			case _: 	FLAGS[flag] = setValue

def setFlagRaw(valueInBits):
	if valueInBits.startswith("Ob"):
		valueInBits = valueInBits.remove("Ob")
	
	for bit in range(len(valueInBits)):
		FLAGS[bit] = int(bool(bit))

def setFlags(flagON : list = [], argOFF :list = []):
	for f in flagON: setFlag(f,1)
	for f in argOFF: setFlag(f,0)

def getRequiredFlags(name):
	match(name):
		case "ADC":	return ["CF"]
		case _: return []

#	resetting flags
def clearFlags():
	global FLAGS
	for N in range(16): FLAGS[N] = 0
	setFlag("NT",1)
	setFlag("IO",1)
	setFlag("PL",1)
	setFlag("IF",1)
	setFlag(-2,1)

clearFlags()

def readFlags() -> str:
	result = ""
	for i in FLAGS: result += str(i)
	return result


###################		CONSOLE, SHOW FLAG REGISTER CONTENT		###################		


#	prints flag register
def printFlags():
	result = readFlags()
	dec = bitsToInt(result)
	print(f"FL :  {result}  =  {dec}")

#	print flag register specifically
def printFlagsSpec():
	print("Power	Sign 	Fl. Name	  Set	Meaning\n")
	print(f"15	MD	Mode Flag	  {FLAGS[0]}	1 NATIVE MODE |" + 
       " 0 - EMULAITON MODE (Always 1 on 8086/186, 0 on 286 and later)")
	print(f"14	NT	Nested Task FL	  {FLAGS[1]}	(Always 1 on 8086/186, 0 on"
       + " 286 and later)")
	print(f"13	IO	Mode Flag	  {FLAGS[2]}	(Always 1 on 8086/186, 0 on 286"
       + " and later)")
	print(f"12	PL	Mode Flag	  {FLAGS[3]}	(Always 1 on 8086/186, 0 on 286"
       + " and later)")
	
	print(f"11	OF	Overflow Flag	  {FLAGS[4]}	1 = OV(Overflow) | 0 = NV"
       + " (Not Overflow)")
	print(f"10	DF	Direction flag	  {FLAGS[5]}	1 = DN(Down) | 0 = UP(Up)")
	print(f"9	IF	Interrupt flag	  {FLAGS[6]}	1 = EI(Enable Interrupt) | "
       + "0 = DI(Disable Interrupt)")
	print(f"8	TF	Trap flag 	  {FLAGS[7]}	-")

	print(f"7	SF	Sign flag 	  {FLAGS[8]}	1 = NG(Negative) | 0 = PL(Positive)")
	print(f"6	ZF	Zero flag	  {FLAGS[9]}	1 = NG(Negative) | 0 = PL(Positive)")
	print(f"5	-	Reserved 	  {FLAGS[10]}	-")
	print(f"4	AF	Auxiliary Carry	  {FLAGS[11]}	1 = AC(Auxiliary Carry) | 0 "
       + "= NA(No Auxiliary Carry)")
	
	print(f"3	-	Reserved	  {FLAGS[12]}	-")
	print(f"2	PF	Parity Flag	  {FLAGS[13]}	1 = PE(Parity Even) | 0 = PO(Parity Odd)")
	print(f"1	-	Reserved	  {FLAGS[14]}	1 = Always")
	print(f"0	CF	Carry Flag	  {FLAGS[15]}	1 = CY(Carry) | 0 = NC(No Carry)")


###################		CONSOLE, DESCRIBE FLAG REGISTER FLAGS		###################	


def def_overflow_flag():
	"""
	--- This function holds definiton of flag in flag register | if called, prints it ---
	
	This flag is set when ther result of SIGNED operaiton is beyon the range

	EX - operation of 2 signed 8 bit intigers

	40 + 100 = 0 0100100 + 0 1100100 = 1 0001000

	We don't have enaugh space so the bit from addition OVERFLOWED the sigh flag

	Hence overflow flag is set
	"""
	print(str(def_overflow_flag.__doc__).replace('\t',''))

def def_direction_flag():
	"""
	--- This function holds definiton of flag in flag register | if called, prints it ---

	This flag indicates in which direction strings are red

	TF = 1

	high bits -> small bits

	TF = 0

	small bits -> high bits
	"""
	print(str(def_direction_flag.__doc__).replace('\t',''))

def def_interrupt_flag():
	"""
	--- This function holds definiton of flag in flag register | if called, prints it ---
	
	If this flag is set it would allow to execute interruption caused
	by external devices (mainly to allow for smooth operation of peripherals)
	"""
	print(str(def_interrupt_flag.__doc__).replace('\t',''))

def def_trap_flag():
	"""
	--- This function holds definiton of flag in flag register | if called, prints it ---
	
	This flag indicates that processor would push to stack values of all
	registers (PUSHF & PUSHA)
	"""
	print(str(def_trap_flag.__doc__).replace('\t',''))

def def_sign_flag():
	"""
	--- This function holds definiton of flag in flag register | if called, prints it ---
	
	This flag is set depending on if we treat our number as signed of unsigned
	integer. It matters if we perform operation outside boundaries of normal number,
	because this results in operation on signed numbers instead of unsigned
	"""
	print(str(def_sign_flag.__doc__).replace('\t',''))

def def_auxiliary_carry_flag():
	"""
	--- This function holds definiton of flag in flag register | if called, prints it ---
	
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
	print(str(def_auxiliary_carry_flag.__doc__).replace('\t',''))

def def_parity_flag():
	"""
	--- This function holds definiton of flag in flag register | if called, prints it ---
	
	The sign flag defines if the number of bits in last calculated number is
	even or not

	EX:

	al = 47 -> 0010 1111 -> SF = 0 - num. of '1' in 47 is not even
	"""
	print(str(def_parity_flag.__doc__).replace('\t',''))

def def_carry_flag():
	"""
	--- This function holds definiton of flag in flag register | if called, prints it ---
	
	This flag stores result of arythmetical operations if the result (additional bit)
	couldn't fit in the register on which we perform an opperation

	EX:

	al = 255 | al + 255 (theoretically) = 510

	since that would be 111111110 => 1 11111110

	CF is set to 1 (this additional '1' from the beginning)

	al = 254 (11111110) - remaining parth that could still fit
	"""
	print(str(def_carry_flag.__doc__).replace('\t',''))
