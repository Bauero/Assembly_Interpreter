#from op1arg import PUSH, POP
from stack import saveValueToStack, readFromStack

def EXENOARG(function): pass

def PUSHA():
    order = ["SP","AX","CX","DX","BX","SP","BP","SI","DI"]
    for register in order:
        saveValueToStack(register, 16, updateSP=True)