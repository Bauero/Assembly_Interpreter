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

#	Oznaczenia
#	"#?"    - something need to be added later !!!

#########################	PREPARATION	  #########################
VARIABLES = {}
history = []

from errors import *
from datatypes import Variable
from multipurpose_registers import *
from flag_register import FLAGS, clearFlags, setFlag, setFlags, getRequiredFlags, printFlags, printFlagsSpec
from stack import STACK, stackCount, saveValueToStack, readFromStack, printStack
from extration_of_data import stringToInt, stringNumToList, bitsToInt, textToInt
from bit_operations import bitAddition, bitSubstraction, bitXOR, binaryMultiplication
from registers_operation_check import registerAddressValue, possibleOpperation, additionalOpReq


#########################	FUNCTIONS	#########################

###	TRANSFORMATION & OPPERATIONS


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
		binList = stringNumToList(s,liczba,len(listOfRegisters[r]))

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



if __name__ == "__main__":

	VARIABLES["fck"] = Variable(8,29,"fck")
	VARIABLES["lol"] = Variable(16,8957,"lol")

	#	testowe operaacje   
	#ADD("AX","word 45000")
	#MOV("AH","AL")
	#ADD("BX","0b1111111111111111")
	#INC("BX")
	#INC("BX")
	saveValueToStack('011001')
	saveValueToStack('100001011001')
	

	print("\nSTACK")
	printStack(0,8)

	print("\nREGISTERS")
	printRegisters()

	print("\nFLAGS")
	#printFlags()
	printFlagsSpec()
