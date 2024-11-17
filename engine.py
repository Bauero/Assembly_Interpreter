# from op2arg import *
# from op1arg import *
# from op0arg import *
# from registers_operation_check import MOV
# # from datatypes import Variable
# from multipurpose_registers import printRegisters
# from flag_register import printFlagsSpec
# from stack import saveValueToStack, printStack
from inspect import signature
import time
from queue import Empty


class Engine():
    """
    This class is responsible for execution of instructions within program. It has access
    to virutal hardware, and given the instruction, it executes it, and modifies the registers
    and flags accordingly
    """

    def __init__(self):
        self._prepareFunctions()

    def _prepareFunctions(self):
        """Is responsible for creating an addresable list of function since
        users usualy call funciton by names represented by string and not by
        a name of the function in program itself (which can be the same, but not for 
        the program). This would allow to match between string and a function
        and then execute the command based on the match"""

        self.funtionNameLink = {k:v for k,v in globals().items() if k.isupper()}
        self.funcSignature = {}  # Keeps the function signagure in a human-readible form
        self.funcArguments = {}  # Keeps the information about signature - necessary for the program

        # defining the function signature and default argument types needed
        for f in self.funtionNameLink:
            if type(self.funtionNameLink[f]) != dict:
                # division for arguments
                description = str(signature(self.funtionNameLink[f]))
                self.funcSignature[f] = description
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
                self.funcArguments[f] = info
            else:
                self.funcArguments[f] = "dict"

    def functionExecutor(self, function : str, args : dict ):
        """
        Is called on every line of code - it's job is to execute order from above
        on the memory of our program

        This function links apropriate function with input
        
                                functionExecutor 
        
        Arguments       ----------------------->    Apriopriate function in the program
        
        EX:

        function: 'ADD' | arg1: 'AX' | arg2: 'BX' -----> ADD(r = 'AX', s = 'BX')
        """
        argList = self.funcArguments[function]['arg']

        if argList == None:
            self.funtionNameLink[function]()
        else:
            argListKeys = list(argList.keys())
            if len(argListKeys) == 1:
                self.funtionNameLink[function](args[argListKeys[0]])
            elif len(argListKeys) == 2:
                self.funtionNameLink[function](args[argListKeys[0]],args[argListKeys[1]])
            else:
                raise NotImplementedError