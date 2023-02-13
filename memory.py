class register:

    # value of the register
    value = 0
    registerName = ""
    bitsize = 8
    dividable = False

    #   basic functions (used also in the __init__)
    def add(self, numer):
        self.value = (self.value + numer) % (2 ** self.bitsize)

    def _setName(self, name):
        listaNazw = ["ax","bx","cx","dx"] + ["al","ah","bl","bh","cl",
                    "ch","dl","dh"] + ["si","bi","bp","di"]

        if name not in listaNazw:
            raise NameError
        else:
            self.registerName = name
    
    def _setBiteSize(self, size):

        avalilableSizes = [2 ** i for i in [2,3,4,5,6]]

        if size not in avalilableSizes:
            raise ValueError
        else:
            self.bitsize = size

    def __init__(self, mainLetter : str, additionalLetter : str, 
                 bitSize : int, startingValue : int = 0, dividible = False):
        
        self.add(startingValue)
        self._setName(mainLetter.lower() + additionalLetter.lower())
        self._setBiteSize(bitSize)
        self.mov(startingValue)

        if dividible:
            self.dividable = True
            bits = "{0:016b}".format(startingValue)
            high, low = int(bits[0:9]), int(bits[9:])

            self.upperRegister = register(self.registerName[0],"h",bitSize//2,high)
            self.lowerRegister = register(self.registerName[0],"l",bitSize//2,low)

    #   the rest of the functions (not reqired in __init__)
    def mov(self, value):
        value = 0
        self.add(value)

    def toBinary(self) -> str:
        return bin(self.value)[2:]
    