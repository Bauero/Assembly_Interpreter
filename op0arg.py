#from op1arg import PUSH, POP
from stack import saveValueToStack, readFromStack
from multipurpose_registers import writeIntoRegister, readFromRegister
from extration_of_data import stringToInt, bitsToInt
from flag_register import readFlags, setFlagRaw

def EXENOARG(function): pass

#   Multipurpose registers
def PUSHA() -> None:
    order = ["ESP","EAX","ECX","EDX","EBX","ESP","EBP","ESI","EDI"]
    #order = ["AX","BX","CX","DX"]
    for i in range(len(order)):
        register = order[i]
        value = (bitsToInt(readFromRegister(register)))
        if i < len(order) - 1:
            saveValueToStack(value, 32, updateSP=True)
        else:
            saveValueToStack(value, 32)


def POPA() -> None:
    order = ["EDI","ESI","EBP","ESP","EBX","EDX","ECX","EAX","ESP"]
    for i in range(len(order)):
        register = order[i]
        point = bitsToInt(readFromRegister("SP"))
        value = bitsToInt(readFromStack(point, 32))
        writeIntoRegister(register, value)
        if i < len(order) - 1:
            point -= 32
            writeIntoRegister("SP",point)



#   Flags
def PUSHF() -> None:
    value = bitsToInt(readFlags())
    point = bitsToInt(readFromRegister("ESP"))
    point += 32
    writeIntoRegister("ESP",point)
    saveValueToStack(value, 32)

def POPF() -> None:
    point = bitsToInt(readFromRegister("ESP"))
    value = str(readFromStack(point, 32))
    setFlagRaw(value)
    point -= 32
    writeIntoRegister("ESP",point)
