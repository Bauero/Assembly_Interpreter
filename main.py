"""
############## PL ##############

To jest program który ma za zadanie pomagać w pracy z Assemblerem 16 bit
Celem tego programu będzie zrobienie aplikacji która w okienku wyświetla
Stan naszych rejestrów a następnie dokonuje wpisanych przez nas operacji
Dlatego zadaniem tego kodu będzie wizualizacja zmian poprzez wypisywanie 
tego co dzieje się z naszym kodem

############## EN ##############

This is program which purpose is to help learn 16 bit assembly
The goal is to make an GUI app which, in window, shows status of 
all registers, and then executs the given instructions
Therefore the purpose of this code is to visualize changes made by user
As a possible extenstion, mayby execution of a file may be added later
so the code should allow it

"""

#	Todo
#	√1. dodanie stostu
#	√2. dodanie obsługu odwołań po adresach

#	Oznaczenia
#	"#?"    - something need to be added later !!!

from errors import *
from datatypes import *
from math import ceil

#########################	PREPARATION	  #########################

AX = [Node(0) for _ in range(16)]
AH, AL = AX[:9], AX[9:]
BX = [Node(0) for _ in range(16)]
BH, BL = BX[:9], BX[9:]
CX = [Node(0) for _ in range(16)]
CH, CL = CX[:9], CX[9:]
DX = [Node(0) for _ in range(16)]
DH, DL = DX[:9], DX[9:]

SI = [Node(0) for _ in range(16)]
DI = [Node(0) for _ in range(16)]
SP = [Node(0) for _ in range(16)]
BP = [Node(0) for _ in range(16)]

listOfRegisters = {"AX" : AX, "AH" : AH, "AL" : AL,
				  "BX" : BX, "BH" : BH, "BL" : BL,
				  "CX" : CX, "CH" : CH, "CL" : CL,
				  "DX" : DX, "DH" : DH, "DL" : DL,

				  "SP" : SP, "BP" : BP, "DI" : DI, 
				  "SI" : SI}

regList = list(listOfRegisters.keys())

#	4096 16-bit places 
STACK = [Node(0) for _ in range(65536)]
stackCount = len(STACK)//8

VARIABLES = {}

history = []

#	initialization of a clear register
FLAGS = [0 for _ in range(16)]

#	resetting flags
def clearFlags():
	global FLAGS
	for i in range(16): FLAGS[i] = 0


#########################	FUNCTIONS	#########################


###	OPERATIONS ON REGISTERS


#	set given flag to setValue
def setFlag(flag,setValue):
	match(flag):
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

#	a function which sets given flags on or off
def setFlags(flagON : list = [], argOFF :list = []):
	for f in flagON: setFlag(f,1)
	for f in argOFF: setFlag(f,0)

#?	- to make
def getRequiredFlags(name):
	match(name):
		case "ADC":	return ["CF"]
		case _: return []

#	inputs the restult into register r, bit by bit
def writeIntoRegister(r, resutl):
	#	converstion of the number to list of binary (in str)
	listaDoWpisania = []
	if len(listOfRegisters[r]) == 16:
		listaDoWpisania = list("{0:016b}".format(resutl))
	elif len(listOfRegisters[r]) == 8:
		listaDoWpisania = list("{0:08b}".format(resutl))

	#	update of the register (using int, not string)
	for i in range(-1,-len(listaDoWpisania)-1,-1):
		listOfRegisters[r][i].data = int(listaDoWpisania[i])	

#	return value from the register as a string of bits
def readFromRegister(r):
	result = ""
	for i in listOfRegisters[r]: 
		result += i.printStr()
	return result

def textToInt(text):
	value = ""
	for l in text:
		value += "{0:08b}".format(ord(l))
	return value

#	save value of 'size' into stack
def saveValueToStack(value):		
	multipleOf16 = ceil(len(value) / 16)
	
	for elem in range(multipleOf16):
		spv = bitsToInt(readFromRegister("SP"))

		if len(value) > elem: STACK[spv].data = int(elem)
		else: STACK[spv].data = 0

		spv += 1
		writeIntoRegister("SP",spv)

def readFromStack(index, size = 16):

	ans = ""

	for i in range(index, index + size + 1):
		ans += str(STACK[i].data)

	return ans



###	CHECK & ERROR FINDING


#	if register is capable of holding effective address
def effectiveAddressable(reg:str):
	if reg not in regList:
		raise RegisterNotImplemented
	
	effReg = ["SI","DI","BP","BX"]

	return reg in effReg

#	is given source, a register, [reg] , var , [var], 10, word 10, word var
def registerAddressValue(s : str):
	# 1 - register
	# 2 - [register]
	# 3 - variable
	# 4 - [variable]
	# 5 - value (10)
	# 6 - specfied value (word 10)
	# 7 - specified variable (word var)
	
	brackets = 0        # count of correct brackets
	badBrackets = 0     # wrong brackets in the s
	size = False
	for c in s:
		if "[" == c: brackets += 1
		if "]" == c: brackets += 1
		if c in "}(){": badBrackets += 1

	# correctly initiated addressing mode - true / false
	if brackets == 2 and badBrackets == 0: addressMode = True
	elif brackets == 0 and badBrackets == 0: addressMode = False
	else:   raise EffectiveAddressError


	isValueSize = False
	if "word" in s or "byte" in s: isValueSize = True
	
	varList = list(VARIABLES.keys())

	if isValueSize:
		for v in varList:
			if v in s: return 7		# word var
		return 6					# word 0x10
	else:

		if addressMode:
			inside = s.lstrip().rstrip()[1:-1]

			if inside in varList: return 4      # [var1]
			elif inside in regList:
				if not effectiveAddressable(inside):
					raise RegisterCantEffectiveAddress
				return 2                        # [AX]
			else: raise EffectiveAddresNotExist

		else:
			inside = s.lstrip().rstrip()

			if inside in varList: return 3      # Var1
			elif inside in regList: return 1    # AX
			else: return 5						# 0x10

#	if, for given function, operation is possible
def possibleOpperation( r : str, s : str, a1 = None, a2 = None):
	pair = (a1, a2)
	availablePairs = {(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),
					  (2,1),(2,6),(2,7),(4,1),(4,6),(4,7)}
	specialPairs = {(1,2),(2,1),(2,6),(2,7)}

	if not pair in availablePairs: return False
	if not pair in specialPairs: return True
	else:
		if pair == (1,2):
			if effectiveAddressable(s): return True
			else: return False
		else:
			if effectiveAddressable(r): return True
			else: return False

#	if additional operation requirements are fulfilled
def additionalOpReq(f, r, s, rType, sType):
	match(f):
		case("ADD"): 
			if rType == sType and rType == 1:
				if len(listOfRegisters[r]) < len(listOfRegisters[s]):
					raise RegisterSizeTooSmall
				if r == "SP" or s == "SP":
					raise RegisterNotWritable
		case("SUB"): 
			if rType == sType and rType == 1:
				if len(listOfRegisters[r]) < len(listOfRegisters[s]):
					raise RegisterSizeTooSmall
				if r == "SP" or s == "SP":
					raise RegisterNotWritable
		case("XOR"):
			if rType == sType and rType == 1:
				if r == "SP":
					raise RegisterNotWritable




###	TRANSFORMATION & OPPERATIONS



#	convert a string to an int with given size
def stringToInt(s, size):
	base = 10
	number = s.split(" ")[-1].lower()
	
	if number.startswith("0b"):
		if int(number,2) > 2**size:
			raise NumberTooBig
		base = 2

	elif number.startswith("0x"):
		if number.endswith("h"):
			number = number[:-1]
		if int(number,16) > 2**size:
			raise NumberTooBig
		base = 16
		
	elif number.endswith("h"):
		number = number[:-1]
		number = "0x" + number
		if int(number,16) > 2**size:
			raise NumberTooBig
		base = 16
		
	else:
		if int(number) > 2**size:
			raise NumberTooBig

	return int(number,base)

#	tranform a given numver, to bit value, based on the dest.
def numberToList(s, number:str, boundSize = 16):
	#	transform 'word 0xf2' -> list('0000000011110010')
	#	transform 'byte 0b11' -> list('00000011')
	#	transform 'word 728'  -> list('0000001011011000')
	#	transform '0xf2' -> list('0000000011110010')
	#	transform '0b11' -> list('00000011')
	#	transform '728'  -> list('0000001011011000')
	listToWrite = []
	
	if "byte" in s:
		size = 8
	elif "word" in s:
		size = 16
	else:
		size = boundSize

	value = stringToInt(s, size)

	if size == 8:
		listToWrite = list("{0:08b}".format(value))
	else:
		listToWrite = list("{0:016b}".format(value))

	return listToWrite

#	turn bit
def bitsToInt(bitString : str):
	return int("0b" + bitString,2)

#	determine the maximu size of the operation
def getMaxSize(r, rType):
	match (rType):
		case 1: return len(listOfRegisters[r])
		case 2: return len(listOfRegisters[r])
		case 4: return VARIABLES[r].size

#	gets value based on the destination
def getValue(s, sType, maxSize):
	match (sType):
		case 1:
			return int("0b" + readFromRegister(s),2)
		case 2: 
			for v in VARIABLES:
				if v.address == int("0b" + readFromRegister(s),2):
					return v.address
			raise VariableAddressNotExisting
		case 3: return VARIABLES[s].address
		case 4: return VARIABLES[s[1:-1]].data
		case 5: return stringToInt(s,maxSize)
		case 6: return stringToInt(s,maxSize)
		case 7: return VARIABLES[s.split(" ")[-1]].address

#	saves value in the destination if possible
def saveInDestination(d, dType, value):
	match(dType):
		case 1: writeIntoRegister(d, value)
		case 2:
			reg = d.lstrip().rstrip()[1:-1]
			varAddres = bitsToInt(readFromRegister(reg))
			for v in VARIABLES:
				if VARIABLES[v].address == varAddres:
					VARIABLES[v].data = value
		case 4:
			VARIABLES[d].data = value	

#	add two numbers bit by bit and activate OF flag
def bitAddition(num1:int, num2:int, opSize, flags):
	cfvalue = 1 if "CF" in flags else 0
	result = num1 + num2 + cfvalue
	flagsOn , flagsOff = [], []

	#	set Carry Flag
	if result >= 2**opSize:
		result -= 2**opSize	;	flagsOn.append("CF")
	else:
		flagsOn.append("CF")
	
	#	set Zero Flag
	if result:	flagsOff.append("ZF")
	else: flagsOn.append("ZF")

	#	set Overflow Flag

	setFlags(flagsOn,flagsOff)	

	return result

#?	sub two numbers bit by bit and activate OF flag
def bitSubstraction(num1:int, num2:int, opSize, flags):
	
	result = num1 - num2
	flagsOn , flagsOff = [], []

	#?	flagi do ustawienia
	setFlags(flagsOn,flagsOff)	

	return result

#?	xor two numbers bit by bit and activate OF flag
def bitXOR(num1:int, num2: int, opSize, flags):

	result = num1 ^ num2
	flagsOn , flagsOff = [], []

	#?	flagi do ustawienia
	setFlags(flagsOn,flagsOff)	

	return result

#	binary multiplication
def binaryMultiplication(num1:int, num2: int, opSize, flags):

	result = num1 * num2
	flagsOn , flagsOff = [], []

	#?	flagi do ustawienia
	setFlags(flagsOn,flagsOff)	

	return result


###	EXECUTION BASED ON AMOUT OF ARGUMENTS


#	executes functions which accept 2 arguments
def EXE2ARG(function, r = "", s = ""):

	#	varification the type of the arguments
	rMode = registerAddressValue(r)
	sMode = registerAddressValue(s)

	#	general check - if theoreticaly operation is possible
	if not possibleOpperation(r,s,rMode,sMode):
		raise OperationNotPossible
	
	#?	specified check (due to operation performed)
	name = function.__name__
	additionalOpReq(name, r, s, rMode, sMode)
	
	#	specifies maximum size of the operation (8/16)
	maxSize = getMaxSize(r, rMode)
	
	#	get values no matter where they are stored
	rValue = getValue(r, rMode, maxSize)
	sValue = getValue(s, sMode, maxSize)

	#	does this operation requires taking into accout some flags
	reqFlags = getRequiredFlags(name)

	#	performa opperations
	result = function(rValue, sValue, maxSize, reqFlags)

	#	save into destination
	saveInDestination(r, rMode, result)

#? 	to write
def EXE1ARG(function, s = ""):

	#	verification the type of the arguments
	sMode = registerAddressValue(s)

	#?	verification ???
	name = function.__name__
	additionalOpReq(name, None, s, None, sMode)

	#	specifies maximum size of the operation (8/16)
	maxSize = getMaxSize(s, sMode)

	#	get values no matter where they are stored
	sValue = getValue(s, sMode, maxSize)

	#	does this operation requires taking into accout some flags
	reqFlags = getRequiredFlags(name)

	#	performa opperations
	result = function(sValue, maxSize, reqFlags)

	saveInDestination(s, sMode, result)

#?	to write
def EXENOARG(function): pass


###	INSTRUCTIONS WITH 2 ARGUMETNS


#	copy value from the source to the register
def MOV(r, s):
	#?	indirect addressing is not implemented
	if r not in regList:
		raise RegisterNotImplemented
	
	#	if source is a register itself
	if s in regList:
		if len(listOfRegisters[s]) > len(listOfRegisters[r]):
			raise RegisterTooSmallToMove

		for i in range(-1,-len(listOfRegisters[s]),-1):
			listOfRegisters[r][i].data = listOfRegisters[s][i].data

	else:
		liczba = s.split(" ")[-1].lower()
		binList = numberToList(s,liczba,len(listOfRegisters[r]))

		for i in range(-1,-len(binList),-1):
			listOfRegisters[r][i].data = int(binList[i])

#	add value from the source to the register
def ADD(r, s):
	EXE2ARG(bitAddition, r, s)

#	substract value from source from the register    
def SUB(r, s):
	EXE2ARG(bitSubstraction, r, s)

#	xor values written in the registers
def XOR(r, s):
	EXE2ARG(bitXOR, r, s)

#	bit or
def ORR(r, s): pass


###	INSTRUCTION WITH 1 ARGUMENT


#	increment register by 1 (ADD register, byte 1)
def INC(r):
	ADD(r,"byte 1")

#	decrement register by 1 (SUB register, byte 1)
def DEC(r):
	SUB(r,"byte 1")

def PUSH(r):
	INC(SP)



###	INSTRUCTION WITHOUT ARGUMENT



#	print the value of the registers bitly
def printRegisters():

	vaxbin = ''
	vbxbin = ''
	vcxbin = ''
	vdxbin = ''
	vsibin = ''
	vdibin = ''
	vbpbin = ''
	vspbin = ''
	
	for i in AX:    vaxbin += str(i.printInt())
	for i in BX:    vbxbin += str(i.printInt())
	for i in CX:    vcxbin += str(i.printInt())
	for i in DX:    vdxbin += str(i.printInt())
	for i in SI:    vsibin += str(i.printInt())
	for i in DI:    vdibin += str(i.printInt())
	for i in SP:    vspbin += str(i.printInt())
	for i in BP:    vbpbin += str(i.printInt())


	print("AX : ",vaxbin, " = ",int("0b"+vaxbin,2))
	print("BX : ",vbxbin, " = ",int("0b"+vbxbin,2))
	print("CX : ",vcxbin, " = ",int("0b"+vcxbin,2))
	print("DX : ",vdxbin, " = ",int("0b"+vdxbin,2))
	print("SI : ",vsibin, " = ",int("0b"+vsibin,2))
	print("DI : ",vdibin, " = ",int("0b"+vdibin,2))
	print("SP : ",vspbin, " = ",int("0b"+vspbin,2))
	print("BP : ",vbpbin, " = ",int("0b"+vbpbin,2))

#?
def printStack(start = 0, end = stackCount, step = 1):
	for i in range(start, end, step):
		value = readFromStack(i)
		intValue = stringToInt(value, 16)
		print("{0:04x}".format(i) + f" : {value} = {intValue}")


def printFlags():
	result = ""
	for i in FLAGS: result += str(i)

	dec = bitsToInt(result)

	print(f"FL :  {result}  =  {dec}")

if __name__ == "__main__":

	VARIABLES["fck"] = Variable(8,29,"fck")
	VARIABLES["lol"] = Variable(16,8957,"lol")

	#	testowe operaacje   
	#ADD("AX","49")
	#MOV("AH","AL")
	#ADD("BX","0b1111111111111111")
	#INC("BX")
	#INC("BX")

	print("\nSTACK")
	printStack(0,10)

	print("\nREGISTERS")
	printRegisters()
	printFlags()
