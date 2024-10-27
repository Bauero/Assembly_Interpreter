from datatypes import Node
from errors import RegisterNotImplemented

EAX = [Node(0) for _ in range(32)]
AX, AH, AL = EAX[16:], EAX[16:24], EAX[24:]
EBX = [Node(0) for _ in range(32)]
BX, BH, BL = EBX[16:], EBX[16:24], EBX[24:]
ECX = [Node(0) for _ in range(32)]
CX, CH, CL = ECX[16:], ECX[16:24], ECX[24:]
EDX = [Node(0) for _ in range(32)]
DX, DH, DL = EDX[16:], EDX[16:24], EDX[24:]

SI = [Node(0) for _ in range(32)]
DI = [Node(0) for _ in range(32)]
SP = [Node(0) for _ in range(32)]
BP = [Node(0) for _ in range(32)]

listOfRegisters = {"EAX" : EAX, "AX" : AX, "AH" : AH, "AL" : AL,
				   "EBX" : EBX, "BX" : BX, "BH" : BH, "BL" : BL,
				   "ECX" : ECX, "CX" : CX, "CH" : CH, "CL" : CL,
				   "EDX" : EDX, "DX" : DX, "DH" : DH, "DL" : DL,
				   "SP" : SP, "BP" : BP, "DI" : DI, 
				   "SI" : SI}

regList = list(listOfRegisters.keys())


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

#	if register is capable of holding effective address
def effectiveAddressable(reg:str):
	if reg not in regList:
		raise RegisterNotImplemented
	
	effReg = ["SI","DI","BP","BX"]

	return reg in effReg

def cleanRegister(r):
	# this is equal to xor(ax,ax) - or any other register
	writeIntoRegister(r,0)

def cleanAllRegisters():
	for regiser in regList:
		cleanRegister(regiser)

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
	
	for i in EAX:    vaxbin += str(i.printInt())
	for i in EBX:    vbxbin += str(i.printInt())
	for i in ECX:    vcxbin += str(i.printInt())
	for i in EDX:    vdxbin += str(i.printInt())
	for i in SI:     vsibin += str(i.printInt())
	for i in DI:     vdibin += str(i.printInt())
	for i in SP:     vspbin += str(i.printInt())
	for i in BP:     vbpbin += str(i.printInt())


	print(f"EAX : {vaxbin} = {int('0b'+vaxbin,2)}")
	print(f"EAX : {vbxbin} = {int('0b'+vbxbin,2)}")
	print(f"EAX : {vcxbin} = {int('0b'+vcxbin,2)}")
	print(f"EAX : {vdxbin} = {int('0b'+vdxbin,2)}")
	print(f"EAX : {vsibin} = {int('0b'+vsibin,2)}")
	print(f"EAX : {vdibin} = {int('0b'+vdibin,2)}")
	print(f"EAX : {vspbin} = {int('0b'+vspbin,2)}")
	print(f"EAX : {vbpbin} = {int('0b'+vbpbin,2)}")

cleanAllRegisters()
