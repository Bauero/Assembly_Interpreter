from registers_operation_check import registerAddressValue,\
    additionalOpReq, getValue, saveInDestination, getMaxSize
from flag_register import getRequiredFlags
from op2arg import SUB, ADD
from stack import saveValueToStack


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

	#?	so far i'm not sure if this is needed - leave for later
	#saveInDestination(s, sMode, result)


###	INSTRUCTION WITH 1 ARGUMENT


#	increment register by 1 (ADD register, byte 1)
def INC(r):
	ADD("SP","byte 1")

#	decrement register by 1 (SUB register, byte 1)
def DEC(r):
	SUB(r,"byte 1")

def PUSH(r):
	EXE1ARG(saveValueToStack,r)
