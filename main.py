"""
To jest program który ma za zadanie pomagać w pracy z Assemblerem 16 bit
Celem tego programu będzie zrobienie aplikacji która w okienku wyświetla
Stan naszych rejestrów a następnie dokonuje wpisanych przez nas operacji
zadaniem tego kodu będzie wizualizacja zmian poprzez wypisywanie tego co 
dzieje się z naszym kodem
"""
#   Todo
#   1. dodanie stostu
#   2. dodanie obsługu odwołań po adresach

#   Oznaczenia
#   "#?"    - something need to be added later !!!

from errors import *
from linkedList import *

AX = [Node(0) for _ in range(16)]
AH, AL = AX[:9], AX[9:]
BX = [Node(0) for _ in range(16)]
BH, BL = BX[:9], BX[9:]
CX = [Node(0) for _ in range(16)]
CH, CL = CX[:9], CX[9:]
DX = [Node(0) for _ in range(16)]
DH, DL = DX[:9], DX[9:]
SI = [Node(0) for _ in range(16)]
DI = [Node(0) for _ in range(16)]
BI = [Node(0) for _ in range(16)]
BP = [Node(0) for _ in range(16)]

#?  to implement leater
STACK = []

#   flag register
FLAGS = [Node(0) for _ in range(16)]

listaRejestrow = {"AX" : AX, "AH" : AH, "AL" : AL,
                  "BX" : BX, "BH" : BH, "BL" : BL,
                  "CX" : CX, "CH" : CH, "CL" : CL,
                  "DX" : DX, "DH" : DH, "DL" : DL}

listaRej = list(listaRejestrow.keys())

#   inputs the restult into register r, bit by bit
def writeIntoRegister(r, resutl):
    #   converstion of the number to list of binary (in str)
    listaDoWpisania = []
    if len(listaRejestrow[r]) == 16:
        listaDoWpisania = list("{0:016b}".format(resutl))
    elif len(listaRejestrow[r]) == 8:
        listaDoWpisania = list("{0:08b}".format(resutl))

    #   update of the register (using int, not string)
    for i in range(-1,-len(listaDoWpisania),-1):
        listaRejestrow[r][i].data = int(listaDoWpisania[i])

#   extract value from register 'AX', 'BX' -> "0b1010" & "0b0101"
#   extract + change 'AX', '101110' -> "0b1010" & "0b101110"
def prepToBinConv(n1, n2, argReady):
    sn1 = "0b" + "".join([i.printStr() for i in listaRejestrow[n1]])
    if not argReady:
        sn2 = "0b" + "".join([i.printStr() for i in listaRejestrow[n2]])
    else:
        sn2 = "0b" + n2

    return sn1, sn2

#   add two numbers bit by bit and activate OF flag
def bitAddition(num1:str, num2:str, argReady = False):
    regSize = len(listaRejestrow[num1])
    overFlow = False
    strnum1, strnum2 = prepToBinConv(num1, num2, argReady)

    wynik = int(strnum1,2) + int(strnum2,2)
    if wynik > 2**regSize:
        wynik -= 2**regSize
        overFlow = True

    return overFlow, wynik

#   sub two numbers bit by bit and activate OF flag
def bitSubstraction(num1:str, num2:str, argReady = False):
    regSize = len(listaRejestrow[num1])
    overFlow = False
    strnum1, strnum2 = prepToBinConv(num1, num2, argReady)

    wynik = int(strnum1,2) - int(strnum2,2)
    if wynik < 0:
        wynik += 2**regSize
        overFlow = True
    
    return overFlow, wynik

#   xor two numbers bit by bit and activate OF flag
def bitXOR(num1:str, num2: str, argReady = False):
    regSize = len(listaRejestrow[num1])
    overFlow = False
    strnum1, strnum2 = prepToBinConv(num1, num2, argReady)
    
    wynik = int(strnum1,2) ^ int(strnum2,2)

    return wynik

#   transform 'word 0xf2' -> list('0000000011110010')
#   transform 'byte 0b11' -> list('00000011')
#   transform 'word 728'  -> list('0000001011011000')
def numberToList(s, number:str):
    listToWrite = []
    base = 10
    if "byte" in s:
        
        if number.startswith("0b"):
            if len(s[2:]) > 8:
                raise NumberTooBig
            base = 2

        elif number.startswith("0x"):
            if number.endswith("h"):
                number = number[:-1]
            if len(number[2:]) > 2:
                raise NumberTooBig
            base = 16
            
        elif number.endswith("h"):
            number = number[:-1]
            number = "0x" + number
            if len(number[2:]) > 2:
                raise NumberTooBig
            base = 16
            
        else:
            if int(number) > 255:
                raise NumberTooBig

        listToWrite = list("{0:08b}".format(int(number,base)))
        
        
    elif "word" in s:
        
        if number.startswith("0b"):
            if len(s[2:]) > 16:
                raise NumberTooBig
            base = 2

        elif number.startswith("0x"):
            if number.endswith("h"):
                number = number[:-1]
            if len(number[2:]) > 4:
                raise NumberTooBig
            base = 16
            
        elif number.endswith("h"):
            number = number[:-1]
            number = "0x" + number
            if len(number[2:]) > 4:
                raise NumberTooBig
            base = 16
            
        else:
            if int(number) > 65535:
                raise NumberTooBig

        listToWrite = list("{0:016b}".format(int(number,base)))
    else:
        raise OperandSizeNotSpecified

    return listToWrite

#   copy value from the source to the register
def MOV(r, s):
    #?  indirect addressing is not implemented
    if r not in listaRej:
        raise RegisterNotImplemented
    
    #   if source is a register itself
    if s in listaRej:
        if len(listaRejestrow[s]) > len(listaRejestrow[r]):
            raise RegisterTooSmallToMove

        for i in range(-1,-len(listaRejestrow[s]),-1):
            listaRejestrow[r][i].data = listaRejestrow[s][i].data

    else:
        liczba = s.split(" ")[-1].lower()
        
        binList = numberToList(s,liczba)

        for i in range(-1,-len(binList),-1):
            listaRejestrow[r][i].data = int(binList[i])

#   add value from the source to the register
def ADD(r, s):
    if r not in listaRej:
        raise RegisterNotImplemented
    
    #   if source is a register itself
    if s in listaRej:
        if len(listaRejestrow[s]) > len(listaRejestrow[r]):
            raise RegisterSizeTooSmall
        
        #   reduction of the result to the register size
        OF, wynik = bitAddition(r,s)
        if OF:
            FLAGS[-12].data = 1
        #?  overflow flag needed

        writeIntoRegister(r, wynik)
    
    else:
        liczba = s.split(" ")[-1].lower()
        binList = numberToList(s,liczba)
        liczba2 = "".join(binList)

        #?  overflow flag needed
        OF, wynik = bitAddition(r,liczba2,argReady = True)
        if OF:
            FLAGS[-12].data = 1

        writeIntoRegister(r, wynik)

#   substract value from source from the register    
def SUB(r, s):
    if r not in listaRej:
        raise RegisterNotImplemented
    
    
    #   if source is a register itself
    if s in listaRej:
        if len(listaRejestrow[s]) > len(listaRejestrow[r]):
            raise RegisterSizeTooSmall
        
        #   reduction of the result to the register size + OF flag
        OF, wynik = bitSubstraction(r,s)
        if OF:
            FLAGS[-12].data = 1

        writeIntoRegister(r, wynik)
    else:
        liczba = s.split(" ")[-1].lower()
        binList = numberToList(s,liczba)
        liczba2 = "".join(binList)

        #?  overflow flag needed
        OF, wynik = bitSubstraction(r,liczba2, True)
        if OF:
            FLAGS[-12].data = 1

        writeIntoRegister(r, wynik)

#   increment register by 1 (ADD register, byte 1)
def INC(r):
    ADD(r,"byte 1")

#   decrement register by 1 (SUB register, byte 1)
def DEC(r):
    SUB(r,"byte 1")

def XOR(r,s):

    if r not in listaRej:
        raise RegisterNotImplemented
    
    #   if source is a register itself
    if s in listaRej:
        if len(listaRejestrow[s]) > len(listaRejestrow[r]):
            raise RegisterSizeTooSmall
        
        #   reduction of the result to the register size
        wynik = bitXOR(r,s)
        
        #?  overflow flag needed

        writeIntoRegister(r, wynik)
    
    else:
        liczba = s.split(" ")[-1].lower()
        binList = numberToList(s,liczba)
        liczba2 = "".join(binList)

        #?  overflow flag needed
        wynik = bitXOR(r,liczba2,True)

        writeIntoRegister(r, wynik)

#   print the value of the registers bitly
def printRegisters():

    vaxbin = ''
    vbxbin = ''
    vcxbin = ''
    vdxbin = ''

    for i in AX:
        vaxbin += str(i.printInt())

    for i in BX:
        vbxbin += str(i.printInt())
    
    for i in CX:
        vcxbin += str(i.printInt())
    
    for i in DX:
        vdxbin += str(i.printInt())


    print("AX : ",vaxbin, " = ",int("0b"+vaxbin,2))
    print("BX : ",vbxbin, " = ",int("0b"+vbxbin,2))
    print("CX : ",vcxbin, " = ",int("0b"+vcxbin,2))
    print("DX : ",vdxbin, " = ",int("0b"+vdxbin,2))

if __name__ == "__main__":

    #   testowe operaacje   
    MOV("BX","byte 10")
    MOV("AX","BX")
    MOV("AX","word 18")
    MOV("AX","word 0x98f")
    ADD("AX","BX")
    ADD("BL","byte 12")
    MOV("CX","word 128")
    DEC("CX")
    XOR("CX","CX")
    INC("DX")
    
    printRegisters()
    