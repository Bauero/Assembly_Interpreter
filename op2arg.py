from errors import OperationNotPossible
from bit_operations import bitAddition, bitSubstraction, bitXOR
from registers_operation_check import registerAddressValue, possibleOpperation,\
    additionalOpReq, getValue, saveInDestination, getMaxSize
from flag_register import getRequiredFlags

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
