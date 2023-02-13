"""
To jest program który ma za zadanie pomagać w pracy z Assemblerem 16 bit
Celem tego programu będzie zrobienie aplikacji która w okienku wyświetla
Stan naszych rejestrów a następnie dokonuje wpisanych przez nas operacji
zadaniem tego kodu będzie wizualizacja zmian poprzez wypisywanie tego co dzieje się z naszym kodem
"""

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

listaRejestrow = {"AX" : AX, "AH" : AH, "AL" : AL,
                  "BX" : BX, "BH" : BH, "BL" : BL,
                  "CX" : CX, "CH" : CH, "CL" : CL,
                  "DX" : DX, "DH" : DH, "DL" : DL}

def mov(r, s):
    listaRej = list(listaRejestrow.keys())
    if r not in listaRej:
        raise RegisterNotImplemented
    
    if s in listaRej:
        if len(listaRejestrow[s]) > len(listaRejestrow[r]):
            raise RegisterTooSmallToMove

        for i in range(-1,-len(listaRejestrow[s]),-1):
            listaRejestrow[r][i].data = listaRejestrow[s][i].data

    else:
        listaDoWpisania = []
        liczba = s.split(" ")[-1].lower()
        if "byte" in s:
            try:
                podstawa = 10

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
                    if len(liczba[2:]) > 3:
                        raise NumberTooBig

                listaDoWpisania = list("{0:08b}".format(int(liczba,podstawa)))
            except:
                raise WrongNumberBase
        
        elif "word" in s:
            try:
                podstawa = 10

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
                    if len(liczba[2:]) > 5:
                        raise NumberTooBig

                listaDoWpisania = list("{0:016b}".format(int(liczba,podstawa)))
            except:
                raise WrongNumberBase


        for i in range(-1,-len(listaDoWpisania),-1):
            listaRejestrow[r][i].data = int(listaDoWpisania[i])
        
mov("BX","byte 10")
mov("AX","BX")
mov("AX","word 18")
mov("AX","word 0x98f")

napis1 = "BX : "
napis2 = "AX : "


for i in BX:
    napis1 += str(i.printInt())

for i in AX:
    napis2 += str(i.printInt())

print(napis1)
print(napis2)
input()