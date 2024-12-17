"""
This file stores all instructions which are responsible for setting a speciphic flags in
procesor
"""

from hardware_registers import HardwareRegisters
from flag_register import FlagRegister
from stack import Stack
from datatypes import Data

def CLC(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        **kwargs):
    """CLEAR CARRY FLAG - This instruction sets carry flag to 0"""

    CLC.__setattr__('params_range', [])
    CLC.__setattr__('allowed_params_combinations', [])

    FlagRegister.setFlag("CF", 0)
    return None

def STC(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        **kwargs):
    """SET CARRY FLAG - This instruction sets carry flag to 1"""

    STC.__setattr__('params_range', [])
    STC.__setattr__('allowed_params_combinations', [])

    FlagRegister.setFlag("CF", 0)
    return None

def CMC(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        **kwargs):
    """COMPLEMENT CARRY FLAGA - This instruction reverses value of carry flag"""

    CMC.__setattr__('params_range', [])
    CMC.__setattr__('allowed_params_combinations', [])

    FlagRegister.setFlag("CF", not FlagRegister.readFlag("CF"))
    return None