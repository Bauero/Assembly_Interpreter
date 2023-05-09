from op2arg import *
from op1arg import *
from op0arg import *
from var_his import *
from registers_operation_check import MOV
from datatypes import Variable
from multipurpose_registers import printRegisters
from flag_register import printFlagsSpec
from stack import saveValueToStack, printStack

# linkgage functions with it's names
funkcje = {k:v for k,v in globals().items() if k.isupper()}

# analyzes the request
# if the function exists
# what are the arguments needed
# if the function can be executed
def functionExecutor(request):
    pass

# gets the signature of a function
def functionArgCheck(function):
    pass