"""
To jest program który ma za zadanie pomagać w pracy z Assemblerem 16 bit
Celem tego programu będzie zrobienie aplikacji która w okienku wyświetla
Stan naszych rejestrów a następnie dokonuje wpisanych przez nas operacji
zadaniem tego kodu będzie wizualizacja zmian poprzez wypisywanie tego co dzieje się z naszym kodem
"""

#to jest wersja najbardziej podstawowa

lista_rozk_barg = ["ret"]
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

class InvalidAmountOfArguments (Exception):
    pass

while True:

    rozkaz, argumenty = None, None

    polecenie = input(">>> ").rstrip().lstrip()
    try:
        rozkaz, *argumenty = polecenie.split(" ")
    except ValueError:
        print("Błąd polecenia !!! - wprowadź poprawne polecenie")
        break

    argumenty = argumenty[0].split(",")

    match rozkaz:

        case "mov":
            if len(argumenty) != 2:
                raise InvalidAmountOfArguments
            
            if ()

