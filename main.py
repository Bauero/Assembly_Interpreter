"""
############## PL ##############

To jest program który ma za zadanie pomagać w pracy z Assemblerem 16 bit
Celem tego programu będzie zrobienie aplikacji która w okienku wyświetla
Stan naszych rejestrów a następnie dokonuje wpisanych przez nas operacji
Dlatego zadaniem tego kodu będzie wizualizacja zmian poprzez wypisywanie 
tego co dzieje się z naszym kodem

############## EN ##############

This is program which purpose is to help learn 16 bit assembly
The goal is to make an GUI app which, in window, shows status of 
all registers, and then executs the given instructions
Therefore the purpose of this code is to visualize changes made by user
As a possible extenstion, mayby execution of a file may be added later
so the code should allow it

"""

#	Oznaczenia
#	"#?"    - something need to be added later !!!

#########################	IMPORT NEEDED MODULES	  #########################


from engine import *
from multipurpose_registers import writeIntoRegister



#########################	  LAUNCH WINDOW APP		  #########################




if __name__ == "__main__":

	VARIABLES["fck"] = Variable(8,29,"fck")
	VARIABLES["lol"] = Variable(16,8957,"lol")

	#	testowe operaacje   
	ADD("AX","word 45000")
	MOV("AH","AL")
	ADD("BX","0b1111111111111111")
	INC("BX")
	INC("BX")
	#saveValueToStack('011001',8)
	#saveValueToStack('100001011001')
	MOV("SP","0")
	PUSH("AX")
	INC("SP")
	

	print("\nSTACK")
	printStack(0,8)

	print("\nREGISTERS")
	printRegisters()

	print("\nFLAGS")
	#printFlags()
	printFlagsSpec()
