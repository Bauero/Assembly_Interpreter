from flag_register import setFlags

#	add two numbers bit by bit and activate OF flag
def bitAddition(num1:int, num2:int, opSize, flags):
	cfvalue = 1 if "CF" in flags else 0
	result = num1 + num2 + cfvalue
	flagsOn , flagsOff = [], []

	#	set Carry Flag
	if result >= 2**opSize:
		result -= 2**opSize
		flagsOn.append("CF")
	else:
		flagsOff.append("CF")
	
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
