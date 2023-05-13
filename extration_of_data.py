from errors import NumberTooBig

#	convert a string to an int with given size
def stringToInt(s, size) -> int:
	base = 10
	number = s.split(" ")[-1].lower()
	
	if number.startswith("0b"):
		if int(number,2) > 2**size:
			raise NumberTooBig
		base = 2

	elif number.startswith("0x"):
		if number.endswith("h"):
			number = number[:-1]
		if int(number,16) > 2**size:
			raise NumberTooBig
		base = 16
		
	elif number.endswith("h"):
		number = number[:-1]
		number = "0x" + number
		if int(number,16) > 2**size:
			raise NumberTooBig
		base = 16
		
	else:
		if int(number) > 2**size:
			raise NumberTooBig

	return int(number,base)


#	tranform a given numver, to bit value, based on the dest.
def stringNumToList(s : str, number:str, boundSize : int = 16):
	#	transform 'word 0xf2' -> list('0000000011110010')
	#	transform 'byte 0b11' -> list('00000011')
	#	transform 'word 728'  -> list('0000001011011000')
	#	transform '0xf2' -> list('0000000011110010')
	#	transform '0b11' -> list('00000011')
	#	transform '728'  -> list('0000001011011000')
	listToWrite = []
	
	if "byte" in s:
		size = 8
	elif "word" in s:
		size = 16
	else:
		size = boundSize

	value = stringToInt(number, size)

	if size == 8:
		listToWrite = list("{0:08b}".format(value))
	else:
		listToWrite = list("{0:016b}".format(value))

	return listToWrite

def stringToNum(text : str, size : str):

	if size == 16: size = "word"
	else: size = "byte"

	return "".join(stringNumToList(size,text))

#	
def bitsToInt(bitString : str):
	return int("0b" + bitString,2)

def textToInt(text : str):
	value = ""
	for l in text:
		value += "{0:08b}".format(ord(l))
	return value
