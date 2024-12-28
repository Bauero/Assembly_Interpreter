from errors import OperationNotPossible
from assembly_instructions.bit_operations import bitAddition, bitSubstraction, bitXOR
from registers_operation_check import registerAddressValue, possibleOpperation,\
    additionalOpReq, getValue, saveInDestination, getMaxSize
from flag_register import getRequiredFlags

#	executes functions which accept 2 arguments
def EXE2ARG(function, r : str = "", s : str = "") -> None:

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
def ADD(r : str , s : str) -> None:
	EXE2ARG(bitAddition, r, s)

#	substract value from source from the register    
def SUB(r : str, s : str) -> None:
	EXE2ARG(bitSubstraction, r, s)

#	xor values written in the registers
def XOR(r : str, s : str) -> None:
	EXE2ARG(bitXOR, r, s)

#	bit or
def ORR(r : str, s : str) -> None: pass
