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
defFunctions = {k:v for k,v in globals().items() if k.isupper()}
funcArguments = {}

# defining the function signature and default argument types needed
for f in defFunctions:
    if type(defFunctions[f]) != dict:
        sgt = str(signature(defFunctions[f]))[1:-1].split(", ")
        for element in range(len(sgt)):
            if "=" in sgt[element]:
                end = sgt[element].index('')
                sgt[element] = sgt[element][:end+1]

        funcArguments[f] = dict()
        for g in sgt:
            if g == '':
                continue
            sig = str(signature(defFunctions[f]).parameters[g].annotation.__name__)
            funcArguments[f][g] = sig
    else:
        funcArguments[f] = "dict"


# analyzes the request
# if the function exists
# what are the arguments needed
# if the function can be executed
def functionExecutor(request):
    pass

# gets the signature of a function
def functionArgCheck(function):
    pass