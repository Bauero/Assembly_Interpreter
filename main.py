#########################	IMPORT NEEDED MODULES	  #########################


from engine import *


#########################	  LAUNCH WINDOW APP		  #########################




if __name__ == "__main__":

	VARIABLES["sumab"] = Variable(8, 29, "sumab")
	VARIABLES["result"] = Variable(16, 8957, "result")

	#	testowe operaacje   
	# ADD("DX","word 45000")
	functionExecutor('ADD',{'r': 'DX', 's': 'word 45000'})
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
	a = readFlags()
	print(a[0:8] + " " + a[8:16])
	printFlagsSpec()
	
	# PUSHF()

	functionExecutor('PUSHF',{})

	print("\nSTACK")
	printStack(0,8)

	print("\nREGISTERS")
	printRegisters()

	# POPF()

	# print("\nSTACK")
	# printStack(0,8)

	# print("\nREGISTERS")
	# printRegisters() 

	#print("\nFLAGS")
	#printFlagsSpec()
