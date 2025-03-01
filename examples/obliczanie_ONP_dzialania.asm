;______________________________________________________________________________;
; PL                                                                           ;
; Celem tego programu jest umożliwienie użytkownikowi przekształcenia działania;
; zapisanego normalnie na zapis w Odwrotnej Notacji Polskiej (ONP)             ;
; NP:   '2*(8-3)-3*2+10'   ->   '2 8 3 - * 2 3 * - 10 +'                       ;
; Date: 23.02.2025                                                             ;
; Autor:  Piotr Bauer                                                          ;
;_______________________________________________________________________________

org 100h
	
	;robie kopie rejestrow, oraz umieszczam na stosie
	;znak oznaczajacy koniec czysczenia stosu -> (
	push bp	
	push ax
	push bx
	push cx
	push dx
	push si
	push di
	push word 40

	call ent	;nowa linia

	;wczytanie danych od uzytkownika
	wczytanie:
	mov ah,10
	mov dx,instr
	int 21h

	;odfiltrowanie danych
	call poprawnaw	;sprawdzenie poprawnawosci nawiasow

;#################
;	PRZYGOTOWANIE
;#################

	;potrzebuję dwa wskazniki - jeden do wpisanych danych (bx)
	mov bx,instr+2

	;drugi do miejsca gdzie bede zapisywal (bp)
	mov bp,wynik+2

	;oznaka konca liczby jest spacja -> by program popranie
	;wczytal pierwsza liczbe dodam sama spacje
	mov word [bp],32
	inc bp

	;pobieram informacje jak dlugie mam dzialanie (cx)
	mov cx,[instr+1]
	xor ch,ch

	;sprawdzanie poziomu zagniezdzenia (di)
	mov di,poziom

	;ah:
	;kopia liczby podczas operacji oraz przechowywanie informacji
	;ze wpisuje liczbe zmiennoprzec.

	;al:
	;informacja nt poziomu ostatniej operacji na stosie (nic to 0)
	mov ax,0

	;tabela wag
	;^ = 4
	;* = 3
	;/ = 3
	;+ = 2
	;- = 2

;#################
;	TLUMACZENIE NA RPN
;#################

	petla:
		;wczytanie nowej wartosci do dx
		mov dx,[bx]
		xor dh,dh
		
		;czy to > niż liczba (czyli ew. czy to potega)
		cmp dl,57
		jg czy_potega

		;czy jest to dzialanie (znak < 48)
		cmp dl,48
		jl dzialanie

		;czy wpisuje liczbe z kropka/kolejna cyfre liczby
		cmp ah,1
		je niespacja
		
		;czy mam wpisac spacje
		mov si, wpiszsp
		cmp word [si],1
		je spacja
		jmp niespacja

		spacja:
		mov word [bp],32
		inc bp
		mov word [si],0	;przywrocenie flagi

		niespacja:
		
		mov [bp],dl
		inc bp
		jmp powt

		;wybor strategii dzialania
		dzialanie:
			mov ah,0	;czysczenie flagi kropki/cyfr

			cmp dl,40		; (
			je otw_naw
			cmp dl,41		; )
			je zam_naw
			cmp dl,44		; ,
			je przecinek
			cmp dl,46		; .
			je kropka

			;skoro to dzialanie to oznacza wpisanie spacji
			;miedzy liczbami
			mov si,wpiszsp
			mov word [si],1

			cmp dl,47		; /
			je dzielenie
			cmp dl,45		; -
			je odejmowanie
			cmp dl,43		; +
			je dodawanie
			cmp dl,42		; *
			je mnozenie
			
			jmp powt

		dzielenie:
			;podjecie decyzji w zaleznosci od tego co jest juz na stosie
			cmp al,3
			jge dziel_zruc
			jmp dziel_koniec

			;kopia wartosci do ah, zrucenie i zostawienie na stosie "("
			dziel_zruc:
			mov ah,dl
			call czyscst
			xor dx,dx
			mov dl,ah
			push word 40

			;wpisanie na stos naszego nowego dzialania, i ustawienie al
			dziel_koniec:
			push dx
			mov al,3
			jmp powt

		odejmowanie:
			;podjecie decyzji w zaleznosci od tego co jest juz na stosie
			cmp al,2
			jge odjem_zruc
			jmp odjem_koniec

			;kopia wartosci do ah, zrucenie i zostawienie na stosie "("
			odjem_zruc:
			mov ah,dl
			call czyscst
			xor dx,dx
			mov dl,ah
			push word 40

			;wpisanie na stos naszego nowego dzialania, i ustawienie al
			odjem_koniec:
			push dx
			mov al,2
			jmp powt

		dodawanie:
			;podjecie decyzji w zaleznosci od tego co jest juz na stosie
			cmp al,2
			jge dodaj_zruc
			jmp dodaj_koniec

			;kopia wartosci do ah, zrucenie i zostawienie na stosie "("
			dodaj_zruc:
			mov ah,dl
			call czyscst
			xor dx,dx
			mov dl,ah
			push word 40

			;wpisanie na stos naszego nowego dzialania, i ustawienie al
			dodaj_koniec:
			push dx
			mov al,2
			jmp powt

		mnozenie:
			;podjecie decyzji w zaleznosci od tego co jest juz na stosie
			cmp al,3
			jge mnoz_zruc
			jmp mnoz_koniec

			;kopia wartosci do ah, zrucenie i zostawienie na stosie "("
			mnoz_zruc:
			mov ah,dl
			call czyscst
			xor dx,dx
			mov dl,ah
			push word 40

			;wpisanie na stos naszego nowego dzialania, i ustawienie al
			mnoz_koniec:
			push dx
			mov al,3
			jmp powt

		kropka:
			mov ah,1
			mov [bp],dl
			inc bp
			jmp powt

		przecinek:
			mov ah,1
			mov dl,46		;zamiana przecinka na kropkę
			mov [bp],dl
			inc bp
			jmp powt

		otw_naw:
			push dx			;wrzucam na stos nasz nawias
			mov al,0		;w nowym nawiasie beda nowe operacje -> zeruje al
			inc byte [di]	;zwiekszam poziom zagniezdzenia
			jmp powt		

		zam_naw:
			dec byte [di]	;zmiejszam poziom zagniezdzenia
			call czyscst	;czyscze stos
			cmp byte [di],0	;czy poziom zagniezdzenia to 0?
			je powt

			;jeśli poziom zagniezdzenia to nie 0 to ustawiam al adekwatnie do
			;ostatniej operacji znajujacej sie na stosie
			mov si,sp
			mov si,[si]			; zastąpienie adresu zawartościa
			cmp si,47			; /
			je ost_dziel_mnoz
			cmp si,45			; -
			je ost_dod_odj
			cmp si,43			; +
			je ost_dod_odj
			cmp si,42			; *
			je ost_dziel_mnoz
			
			ost_dziel_mnoz:
			mov al,3
			jmp powt

			ost_dod_odj:
			mov al,2
			jmp powt

		;potegowanie do zrobienia
		czy_potega:

		powt:
			inc bx		;sprawdz nastepny znak dzialania
			dec cl		;zmniejsz wartosc petli
			cmp cl,0	;jesli juz nie ma znakow to koniec petli
			jg petla

	
	;zrzucanie pozostalych dzialan ze stosu
	call czyscst

;#################
;	OBLICZANIE LICZBY
;#################

	mov di,0			;czyszcze poziom zagniezdzenia

	liczenie:
		mov si,wynik+1
		mov ax,[si]
		add si,ax		;teraz bp wskazuje na ostatni el. dzialania

		;teraz następuje rezerwowanie miejsca na stosie na dzialania
		;oraz liczby wpisywane na stos
		sub sp,2
		mov bp,sp	;bp wskazuje na miejsce gdzie wpisuje liczby na stos
		sub sp,20
		mov bx,sp	;bx wskazuje na miejsce gdzie wpisuje dzialania

		mov ax,0	;ax wskazuje ilość liczby które mam już do dzialania

		

		

	;Wyświetlenie wynku
	call ent
	mov ah,9
	mov dx,wynik+2
	int 21h

	koniec:
	;czyszczenie stosu
	pop di
	pop si
	pop dx
	pop cx
	pop bx
	pop ax
	pop bp

	;zakonczenie dzialania programu
	mov ax,4c00h
	int 21h


;#################
;	DEFINICJE
;#################


;taktyczny enter
ent:
	mov ah,2
	mov dl,10
	int 21h
ret

;czysczenie stosu do natrafienia na "("
czyscst:
	pop dx
	czysczenie:
		mov si,sp
		cmp word [si],40
		je nieczysc
		mov si,[si]
		mov word [bp],si
		inc bp
		add sp,2
		jmp czysczenie
	nieczysc:
	add sp,2
	push dx
ret

poprawnaw:
	mov bp,instr+1
	mov cx,[bp]	;wczytanie ilosci wpisanych znakow
	xor ch,ch
	inc bp
	xor ax,ax
	xor dx,dx
	mov al,1

	sprawdz:
		mov dx,[bp]
		xor dh,dh

		cmp dl,40
		je nawotw
		cmp dl,41
		je nawzam

		jmp nowespr

		nawotw:
		add al,1
		jmp gzero

		nawzam:
		sub al,1

		gzero:
		cmp al,0
		jg nowespr
		mov cx,0

		nowespr:
		inc bp
		loop sprawdz

	

	cmp al,1
	je dobrze

	call ent
	mov ah,9
	mov dx,zlenawiasy
	int 21h
	call ent
	add sp,2
	xor ax,ax
	xor bp,bp
	xor cx,cx
	jmp wczytanie

	;kod wykona sie jesli dobrze wpisalem dzialanie
	dobrze:
	xor ax,ax
	xor bx,bx
	xor bp,bp
	xor cx,cx
ret

saliczby:
	mov bp,instr+1
	mov cx,[bp]	;wczytanie ilosci wpisanych znakow
	xor ch,ch
	inc bp
	mov ax,0

	szukajliczb:
		mov dx,[bp]
		xor dh,dh

		cmp dl,48
		jb noweszukanie

		cmp dl,57
		ja noweszukanie

		mov al,1
		mov cx,0

		noweszukanie:
		inc bp
		loop szukajliczb

	cmp al,1
	je mamyliczby

	call ent
	mov ah,2
	mov dx,niemaliczb
	int 21h
	call ent
	add sp,2
	jmp wczytanie

	;kod wykona sie jesli dobrze wpisalem dzialanie
	mamyliczby:
	xor ax,ax
	xor bx,bx
	xor bp,bp
	xor cx,cx
ret

;#################
;	ZMIENNE
;#################


;dzialanie wpisywane przez uzytkownika
instr dw 25
	  dw 0
	  times 26 dw "$"
	  
;wynik dzialania naszego programu
wynik dw 30
	  dw 0
	  times 31 dw "$"

;przechowywanie poziomu zagniezdzenia nawiasow
poziom db 0

;przechowywanie flagi wpisywanie liczby
wpiszsp db 0

;estetyczne "rowna sie"
rownasie dw " = $"

;zmienna przechowujaca wynik naszego dzialania
suma dw 0

;zmienna przechowywujaca dlugosc ostatniej wpisaywanje liczby
dlliczba dw 0



;###############
;	INFO O BLEDACH
;###############

zlenawiasy dw "Zle wpisano nawiasy!!! - popraw je$"
niemaliczb dw "We wpisanym dzialaniu nie ma liczb!!!$"
dzieliszzero dw "We wpisanym dzialaniu wystepuje dzielenie przez 0 !!!$"
dzniepopr dw "Wpisane dzialania zawieraja blad logiczny (np. + bez liczby)$"