#from op1arg import PUSH, POP
from stack import saveValueToStack, readFromStack
from multipurpose_registers import writeIntoRegister, readFromRegister
from extration_of_data import stringToInt, bitsToInt
from flag_register import readFlags, setFlagRaw

def EXENOARG(function): pass

#   Multipurpose registers
def PUSHA():
    order = ["SP","AX","CX","DX","BX","SP","BP","SI","DI"]
    #order = ["AX","BX","CX","DX"]
    for i in range(len(order)):
        register = order[i]
        value = (bitsToInt(readFromRegister(register)))
        if i < len(order) - 1:
            saveValueToStack(value, 16, updateSP=True)
        else:
            saveValueToStack(value, 16)
    

def POPA():
    order = ["DI","SI","BP","SP","BX","DX","CX","AX","SP"]
    for i in range(len(order)):
        register = order[i]
        point = bitsToInt(readFromRegister("SP"))
        value = bitsToInt(readFromStack(point, 16))
        writeIntoRegister(register, value)
        if i < len(order) - 1:
            point -= 16
            writeIntoRegister("SP",point)



#   Flags
def PUSHF():
    value = bitsToInt(readFlags())
    point = bitsToInt(readFromRegister("SP"))
    point += 16
    writeIntoRegister("SP",point)
    saveValueToStack(value, 16)

def POPF():
    point = bitsToInt(readFromRegister("SP"))
    value = str(readFromStack(point, 16))
    setFlagRaw(value)
    point -= 16
    writeIntoRegister("SP",point)
