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
#	2. dodanie obsługu odwołań po adresach

#	Oznaczenia
#	"#?"    - something need to be added later !!!

from errors import *
from datatypes import *

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

STACK = [Node(0) for _ in range(16*256)]
VARIABLES = {}

history = []

#	flag register
FLAGS = []
#	initialization of a clear register
def clearFlags():
	global FLAGS
	FLAGS = [Node(0) for _ in range(16)]
clearFlags()


#########################	FUNCTIONS	#########################


###	OPERATIONS ON REGISTERS


#	a function which sets given flags to setValue
def setFlags(*arg, setValue : bool = True):
	for f in arg:
		match(f):
			case "NT":  FLAGS[-15].data = int(setValue)
			case "IO":  FLAGS[-14].data = int(setValue)
			case "PL":  FLAGS[-13].data = int(setValue)
			case "OF":  FLAGS[-12].data = int(setValue)
			case "DF":  FLAGS[-11].data = int(setValue)
			case "IF":  FLAGS[-10].data = int(setValue)
			case "TF":  FLAGS[-9 ].data = int(setValue)
			case "SF":  FLAGS[-8 ].data = int(setValue)
			case "ZF":  FLAGS[-5 ].data = int(setValue)
			case "PF":  FLAGS[-3 ].data = int(setValue)
			case "CF":  FLAGS[-1 ].data = int(setValue)

#	inputs the restult into register r, bit by bit
def writeIntoRegister(r, resutl):
	#	converstion of the number to list of binary (in str)
	listaDoWpisania = []
	if len(listOfRegisters[r]) == 16:
		listaDoWpisania = list("{0:016b}".format(resutl))
	elif len(listOfRegisters[r]) == 8:
		listaDoWpisania = list("{0:08b}".format(resutl))

	#	update of the register (using int, not string)
	for i in range(-1,-len(listaDoWpisania),-1):
		listOfRegisters[r][i].data = int(listaDoWpisania[i])	


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


###	TRANSFORMATION & OPPERATIONS


#	tranform a given numver, to bit value, based on the dest.
def numberToList(r, s, number:str):
	#	transform 'word 0xf2' -> list('0000000011110010')
	#	transform 'byte 0b11' -> list('00000011')
	#	transform 'word 728'  -> list('0000001011011000')
	#	transform '0xf2' -> list('0000000011110010')
	#	transform '0b11' -> list('00000011')
	#	transform '728'  -> list('0000001011011000')
	listToWrite = []
	base = 10
	size = 0
	if "byte" in s:
		size = 8
	elif "word" in s:
		size = 16
	else:
		size = len(listOfRegisters[r])
	
	if number.startswith("0b"):
		if int(number,2) >= 2**size:
			raise NumberTooBig
		base = 2

	elif number.startswith("0x"):
		if number.endswith("h"):
			number = number[:-1]
		if int(number,16) >= 2**size:
			raise NumberTooBig
		base = 16
		
	elif number.endswith("h"):
		number = number[:-1]
		number = "0x" + number
		if int(number,16) >= 2**size:
			raise NumberTooBig
		base = 16
		
	else:
		if int(number) >= 2**size:
			raise NumberTooBig

	if size == 8:
		listToWrite = list("{0:08b}".format(int(number,base)))
	else:
		listToWrite = list("{0:016b}".format(int(number,base)))

	return listToWrite

#	extract value from register 'AX', 'BX' -> "0b1010" & "0b0101"
#	extract + change 'AX', '101110' -> "0b1010" & "0b101110"
def prepToBinConv(n1, n2, argReady):
	sn1 = "0b" + "".join([i.printStr() for i in listOfRegisters[n1]])
	if not argReady:
		sn2 = "0b" + "".join([i.printStr() for i in listOfRegisters[n2]])
	else:
		sn2 = "0b" + n2

	return sn1, sn2

#	add two numbers bit by bit and activate OF flag
def bitAddition(num1:str, num2:str, argReady = False):
	regSize = len(listOfRegisters[num1])
	strnum1, strnum2 = prepToBinConv(num1, num2, argReady)

	wynik = int(strnum1,2) + int(strnum2,2)
	if wynik > 2**regSize:
		wynik -= 2**regSize
		setFlags("OF")

	return wynik

#	sub two numbers bit by bit and activate OF flag
def bitSubstraction(num1:str, num2:str, argReady = False):
	regSize = len(listOfRegisters[num1])
	strnum1, strnum2 = prepToBinConv(num1, num2, argReady)

	wynik = int(strnum1,2) - int(strnum2,2)
	if wynik < 0:
		wynik += 2**regSize
		setFlags("OF")
	
	return wynik

#	xor two numbers bit by bit and activate OF flag
def bitXOR(num1:str, num2: str, argReady = False):
	regSize = len(listOfRegisters[num1])
	overFlow = False
	strnum1, strnum2 = prepToBinConv(num1, num2, argReady)
	
	wynik = int(strnum1,2) ^ int(strnum2,2)
	if not wynik:
		setFlags("ZF")

	return wynik

#	binary multiplication
def binMUL(num1:str, num2: str, argReady = False):
	regSize = len(listOfRegisters[num1])

	strnum1, strnum2 = prepToBinConv(num1, num2, argReady)

	wynik = int(strnum1,2) * int(strnum2,2)
	
	return 


###	EXECUTION BASED ON AMOUT OF ARGUMENTS


#	executes functions which accept 2 arguments
def EXE2ARG(function, r = "", s = ""):

	# weryfikacja czy mamy do czynienia z rejestrami
	# czy adresami efektywnymi
	rMode = registerAddressValue(r)
	sMode = registerAddressValue(s)

	#	general check
	if not (possibleOpperation(r,s,rMode,sMode)):
		raise OperationNotPossible
	
	#	specified check (due to operation performed)
	match(function.__name__):
		case("MOV"): pass
		case("ADD"): pass
		case("SUB"): pass
		case("MUL"): pass



	#	if source is a register itself
	if s in regList:
		if len(listOfRegisters[s]) > len(listOfRegisters[r]):
			raise RegisterSizeTooSmall
		
		#	reduction of the result to the register size
		wynik = function(r,s)
		
		#?	overflow flag needed

		writeIntoRegister(r, wynik)
	
	else:
		liczba = s.split(" ")[-1].lower()
		binList = numberToList(r,s,liczba)
		liczba2 = "".join(binList)

		#?	overflow flag needed
		wynik = function(r,liczba2,True)

		writeIntoRegister(r, wynik)

#? 	to write
def EXE1ARG(function, s = ""): pass

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
		
		binList = numberToList(r,s,liczba)

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


###	INSTRUCTION WITH 1 ARGUMENT


#	increment register by 1 (ADD register, byte 1)
def INC(r):
	ADD(r,"byte 1")

#	decrement register by 1 (SUB register, byte 1)
def DEC(r):
	SUB(r,"byte 1")


###	INSTRUCTION WITHOUT ARGUMENT



def ToDo():
	#?	- to implement
	def MUL(s): pass
	
	#?	- to implement
	def DIV(s): pass

	#?	- to implement
	def RET(): pass

	#?	- to implement
	def CALL(d): pass

	#?	- to implement
	def LOOP(d): pass

	#?	- to implement
	def NEG(r): pass

	#?	- to implement
	def AND(r, s): pass

	#?	- to implement
	def INT(i): pass

	#?	- to implement
	def PUSH(v): pass

	#?	- to implement
	def POP(r, s): pass
	
	#?	- to implement
	def JMP(d): pass

	#?	- to implement
	def JE(d): pass

	#?	- to implement
	def JNE(d): pass

	#?	- to implement
	def JA(d): pass

	#?	- to implement
	def JNA(d): pass

	#?	- to implement
	def JB(d): pass

	#?	- to implement
	def JNB(d): pass

	#?	- to implement
	def JL(d): pass

	#?	- to implement
	def JNL(d): pass

	#?	- to implement
	def JG(d): pass

	#?	- to implement
	def JNG(d): pass

	#?	- to implement
	def JZ(d): pass

	#?	- to implement
	def JC(d): pass

	#?	- to implement
	def JS(d): pass



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

if __name__ == "__main__":

	#	testowe operaacje   
	MOV("BX","byte 10")
	MOV("AX","BX")
	MOV("AX","word 18")
	MOV("AX","word 0x98f")
	ADD("AX","BX")
	ADD("BL","byte 12")
	MOV("CX","word 128")
	DEC("CX")
	XOR("CX","CX")
	INC("DX")
	
	printRegisters()
