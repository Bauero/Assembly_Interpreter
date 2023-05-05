#########################	IMPORT NEEDED MODULES	  #########################


from engine import *


#########################	  LAUNCH WINDOW APP		  #########################




if __name__ == "__main__":

	VARIABLES["fck"] = Variable(8,29,"fck")
	VARIABLES["lol"] = Variable(16,8957,"lol")

	#	testowe operaacje   
	ADD("DX","word 45000")
	MOV("DH","DL")
	ADD("BX","0b1111111111111111")
	INC("BX")
	INC("BX")
	#saveValueToStack('011001',8)
	#saveValueToStack('100001011001')
	
	print("\nSTACK")
	printStack(0,8)

	print("\nREGISTERS")
	printRegisters()

	print("\nFLAGS")
	printFlagsSpec()
	
	PUSHF()

	print("\nSTACK")
	printStack(0,8)

	print("\nREGISTERS")
	printRegisters()

	POPF()

	print("\nSTACK")
	printStack(0,8)

	print("\nREGISTERS")
	printRegisters() 

	#print("\nFLAGS")
	#printFlagsSpec()
