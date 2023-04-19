#from op1arg import PUSH, POP
from stack import saveValueToStack, readFromStack
from multipurpose_registers import writeIntoRegister, readFromRegister
from extration_of_data import stringToInt, bitsToInt
from flag_register import readFlags, FLAGS

def EXENOARG(function): pass

def PUSHA():
    order = ["SP","AX","CX","DX","BX","SP","BP","SI","DI"]
    for register in order:
        value = (bitsToInt(readFromRegister(register)))
        saveValueToStack(value, 16, updateSP=True)

def POPA():
    order = ["DI","SI","BP","SP","BX","DX","CX","AX","SP"]
    for register in order:
        point = stringToInt(readFromRegister("SP"),16)
        value = readFromStack(point, 16)
        writeIntoRegister(register, value)

def PUSHF():
    value = bitsToInt(readFlags())
    saveValueToStack(value, 16, updateSP=True)