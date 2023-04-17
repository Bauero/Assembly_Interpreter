#from op1arg import PUSH, POP
from stack import saveValueToStack, readFromStack
from registers_operation_check import writeIntoRegister, readFromRegister
from extration_of_data import stringToInt

def EXENOARG(function): pass

def PUSHA():
    order = ["SP","AX","CX","DX","BX","SP","BP","SI","DI"]
    for register in order:
        saveValueToStack(register, 16, updateSP=True)

def POPA():
    order = ["DI","SI","BP","SP","BX","DX","CX","AX","SP"]
    for register in order:
        point = stringToInt(readFromRegister("SP"),16)
        value = readFromStack(point, 16)
        writeIntoRegister(register, value)
