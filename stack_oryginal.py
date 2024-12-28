from math import ceil
from datatypes import Node
from hardware_registers import readFromRegister, writeIntoRegister
from extration_of_data import bitsToInt, stringToInt, stringToNum

#	4096 16-bit places 
STACK = [Node(0) for _ in range(65536)]
stackCount = len(STACK)//8

#	save value of 'size' into stack
#	size is ceil of value / 16 -> divide by 16
#	and fill with '0' if necessary
def saveValueToStack(value, size = None, flags = None, updateSP = False):		
	if size == None: size = 16
	
	if type(value) == int:
		value = stringToNum(str(value),size)
	else: value = str(value)

	multipleOfSize = ceil(len(value) / size)

	spv = bitsToInt(readFromRegister("SP"))
	
	for elem in range(0,size*multipleOfSize):

		if elem < len(value): STACK[spv].data = int(value[-1-elem])
		else: STACK[spv].data = 0

		spv += 1

	#	should this move stack pointer to next free spot
	if updateSP: writeIntoRegister("SP",spv)

def readFromStack(index, size = 8):
	ans = ""

	for i in range(index, index + size):
		ans += str(STACK[i].data)

	return "".join(list(reversed(ans)))


def printStack(start = 0, end = stackCount, step = 1):
	if end < start:
		start, end = end, start
	for i in range(start, end, step):
		#	because stack is filled left to right we need to reverse it
		value = readFromStack(16*i,16)
		intValue = stringToInt("0b" + value, 16)

		print("{0:04x}".format(2*i).upper() + f" : {value} = {intValue}")

