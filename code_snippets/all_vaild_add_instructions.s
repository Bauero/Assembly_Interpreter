;Register to Register:
;add AX, BX
;add CX, DX
;add SP, BP
;add SI, DI

;Immediate to Register:
;add AX, 1
;add BX, 1234h
;add CX, 0FFh
add DX, -1
add AX, -10h
add AX, 1

;Memory to Register:
;add AX, [BX]
;add BX, [SI]
;add CX, [BP+DI]
;add DX, [1234h]

;Register to Memory:
;add [BX], AX
;add [SI], BX
;add [BP+DI], CX
;add [1234h], DX

;Immediate to Memory:
;add [BX], 1
;add [SI], 1234h
;add [BP+DI], 0FFh
;add [1234h], -1

;Immediate to Accumulator:
;add AL, 1
;add AX, 1234h
;add EAX, 0FFh
;add RAX, -1