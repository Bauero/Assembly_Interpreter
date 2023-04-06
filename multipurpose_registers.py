from datatypes import Node
from errors import RegisterNotImplemented

AX = [Node(0) for _ in range(16)]
AH, AL = AX[:8], AX[8:]
BX = [Node(0) for _ in range(16)]
BH, BL = BX[:8], BX[8:]
CX = [Node(0) for _ in range(16)]
CH, CL = CX[:8], CX[8:]
DX = [Node(0) for _ in range(16)]
DH, DL = DX[:8], DX[8:]

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


cleanAllRegisters()