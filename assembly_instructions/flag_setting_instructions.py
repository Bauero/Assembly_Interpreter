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
        Labels : dict,
        **kwargs):
    """CLEAR CARRY FLAG - This instruction sets carry flag to 0"""

    previous_state = FlagRegister.readFlags()
    FlagRegister.setFlag("CF", 0)
    new_state = FlagRegister.readFlags()

    response = {
        "action" :          "flags_changed",
        "location" :        "CF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

def CLD(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """CLEAR DIRECTION FLAG - This instruction sets direction flag to 0"""

    previous_state = FlagRegister.readFlags()
    FlagRegister.setFlag("DF", 0)
    new_state = FlagRegister.readFlags()

    response = {
        "action" :          "flags_changed",
        "location" :        "DF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

def CLI(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """CLEAR INTERRUPT FLAG - This instruction sets interrupt flag to 0"""

    previous_state = FlagRegister.readFlags()
    FlagRegister.setFlag("IF", 0)
    new_state = FlagRegister.readFlags()

    response = {
        "action" :          "flags_changed",
        "location" :        "IF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

def CMC(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """COMPLEMENT CARRY FLAG - This instruction reverses value of carry flag"""

    previous_state = FlagRegister.readFlags()
    FlagRegister.setFlag("CF", not FlagRegister.readFlag("CF"))
    new_state = FlagRegister.readFlags()

    response = {
        "action" :          "flags_changed",
        "location" :        "CF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

def STC(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """SET CARRY FLAG - This instruction sets carry flag to 1"""

    previous_state = FlagRegister.readFlags()
    FlagRegister.setFlag("CF", 1)
    new_state = FlagRegister.readFlags()
    
    response = {
        "action" :          "flags_changed",
        "location" :        "CF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

def STD(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """SET DIRECTION FLAG - This instruction sets direction flag to 1"""

    previous_state = FlagRegister.readFlags()
    FlagRegister.setFlag("DF", 1)
    new_state = FlagRegister.readFlags()
    
    response = {
        "action" :          "flags_changed",
        "location" :        "DF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

def STI(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """SET INTERRUPT FLAG - This instruction sets interrupt flag to 1"""

    previous_state = FlagRegister.readFlags()
    FlagRegister.setFlag("IF", 1)
    new_state = FlagRegister.readFlags()
    
    response = {
        "action" :          "flags_changed",
        "location" :        "IF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

for fn_name in list(filter(lambda n: n.upper() == n, dir())):
    """Assign all functions the same attributes"""
    fn = locals()[fn_name]
    fn.params_range = [0]
    fn.allowed_params_combinations = [tuple()]
