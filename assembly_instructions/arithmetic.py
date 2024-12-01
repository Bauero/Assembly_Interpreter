# from bit_operations import bitAddition
from hardware_registers import HardwareRegisters
from flag_register import FlagRegister
from stack import Stack
from datatypes import Data

def ADD(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data, 
        **kwargs):
    """This function performs addition"""

    ADD.__setattr__('params_range', [2])
    ADD.__setattr__('allowed_params_combinations', [
        (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
        (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
    ])
    
    #   Adding

    return None