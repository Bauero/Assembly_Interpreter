from registers_operation_check import registerAddressValue,\
    additionalOpReq, getValue, saveInDestination, getMaxSize
from flag_register import getRequiredFlags
from op2arg import SUB, ADD
from stack_oryginal import saveValueToStack, readFromStack
from hardware_registers import readFromRegister
from extration_of_data import bitsToInt


def EXE1ARG(function, s : str = ""):

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

	if name not in ["saveValueToStack"]:
		saveInDestination(s, sMode, result)


###	INSTRUCTION WITH 1 ARGUMENT


#	increment register by 1 (ADD register, byte 1)
def INC(r : str) -> None:
	ADD(r,"byte 1")

#	decrement register by 1 (SUB register, byte 1)
def DEC(r : str) -> None:
	SUB(r,"byte 1")

#	save value to stack
def PUSH(v : str) -> None:
	EXE1ARG(saveValueToStack,v)

#	pop value from stack to the destination d
def POP(d : str) -> None:

	#	verification the type of the arguments
	dMode = registerAddressValue(d)

	#?	verification ???
	additionalOpReq("pop", "stack", d, None, dMode)

	#	specifies maximum size of the operation (8/16)
	maxSize = getMaxSize(d, dMode)
	if type(maxSize) != int: maxSize = 16

	index = bitsToInt(readFromRegister("SP"))

	result = bitsToInt(readFromStack(8*index, maxSize))

	saveInDestination(d, dMode, result)

