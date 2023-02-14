"""
To jest program który ma za zadanie pomagać w pracy z Assemblerem 16 bit
Celem tego programu będzie zrobienie aplikacji która w okienku wyświetla
Stan naszych rejestrów a następnie dokonuje wpisanych przez nas operacji
zadaniem tego kodu będzie wizualizacja zmian poprzez wypisywanie tego co dzieje się z naszym kodem
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

FLAGS = [Node(0) for _ in range(16)]

listaRejestrow = {"AX" : AX, "AH" : AH, "AL" : AL,
                  "BX" : BX, "BH" : BH, "BL" : BL,
                  "CX" : CX, "CH" : CH, "CL" : CL,
                  "DX" : DX, "DH" : DH, "DL" : DL}

listaRej = list(listaRejestrow.keys())

def bitAddition(num1:str, num2:str) -> int:
    strnum1 = "0b" + "".join([i.printStr() for i in listaRejestrow[num1]])
    strnum2 = "0b" + "".join([i.printStr() for i in listaRejestrow[num2]])

    return (int(strnum1,2) + int(strnum2,2)) % 2**len(listaRejestrow[num1])

def bitSubstraction(num1:str, num2:str) -> int:
    regSize = len(listaRejestrow[num1])
    strnum1 = "0b" + "".join([i.printStr() for i in listaRejestrow[num1]])
    strnum2 = "0b" + "".join([i.printStr() for i in listaRejestrow[num2]])

    wynik = int(strnum1,2) + int(strnum2,2)
    if wynik < 0:
        wynik += 2**regSize
    
    return wynik

def numberToList(s, liczba:str):
    listaDoWpisania = []
    podstawa = 10
    if "byte" in s:
        
        if liczba.startswith("0b"):
            if len(s[2:]) > 8:
                raise NumberTooBig
            podstawa = 2

        elif liczba.startswith("0x"):
            if liczba.endswith("h"):
                liczba = liczba[:-1]
            if len(liczba[2:]) > 2:
                raise NumberTooBig
            podstawa = 16
            
        elif liczba.endswith("h"):
            liczba = liczba[:-1]
            liczba = "0x" + liczba
            if len(liczba[2:]) > 2:
                raise NumberTooBig
            podstawa = 16
            
        else:
            if int(liczba) > 255:
                raise NumberTooBig

        listaDoWpisania = list("{0:08b}".format(int(liczba,podstawa)))
        
        
    elif "word" in s:
        
        if liczba.startswith("0b"):
            if len(s[2:]) > 16:
                raise NumberTooBig
            podstawa = 2

        elif liczba.startswith("0x"):
            if liczba.endswith("h"):
                liczba = liczba[:-1]
            if len(liczba[2:]) > 4:
                raise NumberTooBig
            podstawa = 16
            
        elif liczba.endswith("h"):
            liczba = liczba[:-1]
            liczba = "0x" + liczba
            if len(liczba[2:]) > 4:
                raise NumberTooBig
            podstawa = 16
            
        else:
            if int(liczba) > 65535:
                raise NumberTooBig

        listaDoWpisania = list("{0:016b}".format(int(liczba,podstawa)))
        
    return listaDoWpisania

def MOV(r, s):
    #?  indirect addressing is not implemented
    if r not in listaRej:
        raise RegisterNotImplemented
    
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

def ADD(r, s):
    if r not in listaRej:
        raise RegisterNotImplemented
    
    if s in listaRej:
        if len(listaRejestrow[s]) > len(listaRejestrow[r]):
            raise RegisterSizeTooSmall
        
        #   reduction of the result to the register size
        wynik = bitAddition(r,s) % 2**len(listaRejestrow[r])
        #?  overflow flag needed

        #   converstion of the number to list of binary (in str)
        listaDoWpisania = []
        if len(listaRejestrow[r]) == 16:
            listaDoWpisania = list("{0:016b}".format(wynik))
        elif len(listaRejestrow[r]) == 8:
            listaDoWpisania = list("{0:08b}".format(wynik))

        #   update of the register (using int, not string)
        for i in range(-1,-len(listaDoWpisania),-1):
            listaRejestrow[r][i].data = int(listaDoWpisania[i])
    
    else:
        liczba = s.split(" ")[-1].lower()
        binList = numberToList(s,liczba)
        liczba2 = "".join(binList)

        #?  overflow flag needed
        wynik = bitAddition(r,liczba2)

        #   converstion of the number to list of binary (in str)
        listaDoWpisania = []
        if len(listaRejestrow[r]) == 16:
            listaDoWpisania = list("{0:016b}".format(wynik))
        elif len(listaRejestrow[r]) == 8:
            listaDoWpisania = list("{0:08b}".format(wynik))

        #   update of the register (using int, not string)
        for i in range(-1,-len(listaDoWpisania),-1):
            listaRejestrow[r][i].data = int(listaDoWpisania[i])
    
def SUB(r, s):
    if r not in listaRej:
        raise RegisterNotImplemented
    
    if s in listaRej:
        if len(listaRejestrow[s]) > len(listaRejestrow[r]):
            raise RegisterSizeTooSmall
        
        #   reduction of the result to the register size
        wynik = bitSubstraction(r,s)
        #?  overflow flag needed

        #   converstion of the number to list of binary (in str)
        listaDoWpisania = []
        if len(listaRejestrow[r]) == 16:
            listaDoWpisania = list("{0:016b}".format(wynik))
        elif len(listaRejestrow[r]) == 8:
            listaDoWpisania = list("{0:08b}".format(wynik))

        #   update of the register (using int, not string)
        for i in range(-1,-len(listaDoWpisania),-1):
            listaRejestrow[r][i].data = int(listaDoWpisania[i])
    else:
        liczba = s.split(" ")[-1].lower()
        binList = numberToList(s,liczba)
        liczba2 = "".join(binList)

        #?  overflow flag needed
        wynik = bitSubstraction(r,liczba2)

        #   converstion of the number to list of binary (in str)
        listaDoWpisania = []
        if len(listaRejestrow[r]) == 16:
            listaDoWpisania = list("{0:016b}".format(wynik))
        elif len(listaRejestrow[r]) == 8:
            listaDoWpisania = list("{0:08b}".format(wynik))

        #   update of the register (using int, not string)
        for i in range(-1,-len(listaDoWpisania),-1):
            listaRejestrow[r][i].data = int(listaDoWpisania[i])


if __name__ == "__main__":     
    MOV("BX","byte 10")
    MOV("AX","BX")
    MOV("AX","word 18")
    MOV("AX","word 0x98f")
    ADD("AX","BX")
    ADD("BL","byte 12")

    napis1 = "BX : "
    napis2 = "AX : "


    for i in BX:
        napis1 += str(i.printInt())

    for i in AX:
        napis2 += str(i.printInt())

    print(napis1)
    print(napis2)