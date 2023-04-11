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

#	a function which sets given flags on or off
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

#	prints flag register
def printFlags():
	result = ""
	for i in FLAGS: result += str(i)
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
	print(f"0	CF	Parity Flag	  {FLAGS[15]}	1 = CY(Carry) | 0 = NC(No Carry)")
