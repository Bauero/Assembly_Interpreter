"""
This file contains all jump instuctions which are supported in x86 Assembly
"""

from hardware_registers import HardwareRegisters
from flag_register import FlagRegister
from stack import Stack
from datatypes import Data
from errors import LabelNotRecognizedError

################################################################################
#   FUNCTION DEFINITIONS
################################################################################

def JMP(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function performs unconditional jump to """

    argument = kwargs['values']

    if argument not in Labels:
        raise LabelNotRecognizedError

    return {"next_instruction" : Labels[argument]}

################################################################################
#   FUNCTION ATTRIBUTES
################################################################################

JMP.params_range = [1]
JMP.allowed_params_combination = []
