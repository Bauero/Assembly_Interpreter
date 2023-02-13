"""
To jest program który ma za zadanie pomagać w pracy z Assemblerem 16 bit
Celem tego programu będzie zrobienie aplikacji która w okienku wyświetla
Stan naszych rejestrów a następnie dokonuje wpisanych przez nas operacji
zadaniem tego kodu będzie wizualizacja zmian poprzez wypisywanie tego co dzieje się z naszym kodem
"""

from functions import *
from errors import *
from memory import register

#to jest wersja najbardziej podstawowa

pol_bez_arg = [ "ret" ]
#   rejestry wielozadaniowe
rejwielz = ["ax","bx","cx","dx"]
#   podrejestry
podrejestry = ["al","ah","bl","bh","cl","ch","dl","dh"]
#   rejestry dodatkowe
rejdod = ["si","bi","bp","di"]
#   rejestry wielozadaniowe i podrejestry (rejestry wszystkie)
rejwsz = rejwielz + podrejestry + rejdod
#   podział rejestrów (na przyszłość)
subrejestry = {"ax" : ["ah","al"],
               "bx" : ["bh","bl"],
               "cx" : ["ch","cl"],
               "dx" : ["dh","dl"]}

listaRejestrow = {}

for r in rejwielz:
    listaRejestrow[r] = register(r,"",16,dividible=True)
    listaRejestrow[subrejestry[r][0]] = listaRejestrow[r].upperRegister
    listaRejestrow[subrejestry[r][1]] = listaRejestrow[r].lowerRegister

for r in rejdod:
    listaRejestrow[r] = register(r,"",16)

def firstChar(string, char):
    for i in range(len(string)):
        if string[i] == char:
            return i
    return -1

while True:

    #   krojenie rozkazu
    polecenie = input(">>> ").rstrip().lstrip()
    try:
        polecenie.lower()
        sp1 = firstChar(polecenie," ")

        if sp1 == -1:
            raise ValueError

        rozkaz = polecenie[:sp1]
        argumenty = polecenie[sp1+1:]

        if len(argumenty) < 2 and not rozkaz in pol_bez_arg:
            raise InvalidAmountOfArguments
    
        argumenty = argumenty.split(",")
        
    except InvalidAmountOfArguments:
        print("Podano złą liczbę argumentów !!!")
        continue    
    
    except ValueError:
        print("Błąd polecenia !!! - wprowadź poprawne polecenie")
        continue


    #   podjecie dzialania ze względu na operacje do wykonania
    try:
        match rozkaz:

            case "mov":
                if len(argumenty) != 2:
                    raise InvalidAmountOfArguments
                
                if argumenty[0] not in rejwsz:
                    raise InvalidRegister
                
                if not argumenty[1].isalpha():
                    if "byte" in argumenty[1]:
                        liczba = argumenty[1].split(" ")[-1]
                        liczba = int("0b{0:08b}".format(liczba),10)
                        
                    
                    elif "word" in argumenty[1]:
                        pass
                    else:
                        raise InvalidArgumentValue
                
                mov(argumenty[0],argumenty[1],listaRejestrow)

            case "add":
                

                pass

                
    except InvalidAmountOfArguments:
        print("Podano złą ilość argumentów")

    except InvalidRegister:
        print("Podano nieistniejący rejestr")

    except InvalidArgumentValue:
        print("Podano niewłaściwą wartość - jeśli to liczba to sprawdź czy jest" 
              + "proprzedzona rozmiarem 'byte' (8) lub 'word' (16)")

