from op2arg import *
from op1arg import *
from op0arg import *
from var_his import *
from registers_operation_check import MOV
from datatypes import Variable
from multipurpose_registers import printRegisters
from flag_register import printFlagsSpec
from stack import saveValueToStack, printStack
from inspect import signature

# linkgage functions with it's names
funtionNameLink = {k:v for k,v in globals().items() if k.isupper()}
"""Is responsible for creating an addresable list of function since
users usualy call funciton by names represented by string and not by
a name of the function in program itself (which can be the same, but not for 
the program). This would allow to check the executed string for a function
and then execute the command based on the match"""

funcSignature = {}
"""Keeps the function signagure in a human-readible form"""
funcArguments = {}
"""Keeps the information about signature - necessary for the program"""

# defining the function signature and default argument types needed
for f in funtionNameLink:
    if type(funtionNameLink[f]) != dict:
        # division for arguments
        description = str(signature(funtionNameLink[f]))
        funcSignature[f] = description
        wynik = description.split(" -> ")
        zwrot = wynik[-1] if "->" in description else None
        argm = wynik[0].replace("(","").replace(")","").split(", ")
        argtyp = [
            e.split(": ") if ":" in e else [e,"any"] for e in argm if e != ""
            ]
        info = {}
        if argtyp == []:
            info["arg"] = None
        else:
            info["arg"] = {}
            for e in argtyp:
                if " = " in e[1]:
                    para = e[1].split(" = ")
                    info["arg"][e[0]] = {para[0] : para[1] if para[1] != "''" else ""}
                else:
                    info["arg"][e[0]] = e[1]
        info["ret"] = zwrot
        funcArguments[f] = info
    else:
        funcArguments[f] = "dict"

def functionExecutor(request : str):
    """
    Is called on every line of code - it's job is to oreder what to do with
    ordef from the program or user
    """
    pass
