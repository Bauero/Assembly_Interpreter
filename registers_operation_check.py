from errors import EffectiveAddressError, RegisterCantEffectiveAddress,\
    EffectiveAddresNotExist, RegisterSizeTooSmall, RegisterNotWritable, \
	VariableAddressNotExisting, RegisterNotImplemented, RegisterTooSmallToMove
from var_his import VARIABLES
from multipurpose_registers import effectiveAddressable, regList, listOfRegisters,\
    writeIntoRegister, readFromRegister
from extration_of_data import stringToInt, bitsToInt, stringNumToList



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
