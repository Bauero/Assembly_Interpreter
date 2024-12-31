"""
This file contains all jump instuctions which are supported in x86 Assembly
"""

from hardware_registers import HardwareRegisters
from flag_register import FlagRegister
from stack import Stack
from datatypes import Data
from helper_functions import convert_number_to_int_with_binary_capacity

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
    """This function performs unconditional jump to label"""

    label = kwargs['values'][0]

    return {"next_instruction" : label}

def JZ(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if last operation was equal zero -> ZF=1"""

    label = kwargs['values'][0]
    
    if FlagRegister.readFlag("ZF"):
        return {"next_instruction" : label}

def JE(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if numbers are equal -> ZF=1"""

    label = kwargs['values'][0]
    
    if FlagRegister.readFlag("ZF"):
        return {"next_instruction" : label}

def JNZ(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if last operation wasn't equal to zero -> ZF=0"""

    label = kwargs['values'][0]
    
    if not FlagRegister.readFlag("ZF"):
        return {"next_instruction" : label}

def JNE(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if numbers aren't equal -> ZF=0"""

    label = kwargs['values'][0]
    
    if not FlagRegister.readFlag("ZF"):
        return {"next_instruction" : label}
    
    if not FlagRegister.readFlag("SF"):
        return {"next_instruction" : label}

def JA(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if last result was above zero -> CF=0 AND ZF=0"""

    label = kwargs['values'][0]

    CF = FlagRegister.readFlag("CF")
    ZF = FlagRegister.readFlag("ZF")
    
    if not (CF or ZF):
        return {"next_instruction" : label}

def JNBE(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if last result not below or equal 0 -> CF=0 AND ZF=0"""

    label = kwargs['values'][0]

    CF = FlagRegister.readFlag("CF")
    ZF = FlagRegister.readFlag("ZF")
    
    if not (CF or ZF):
        return {"next_instruction" : label}

def JAE(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if above or equal -> CF=0"""

    label = kwargs['values'][0]
    
    if not FlagRegister.readFlag("CF"):
        return {"next_instruction" : label}

def JNB(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if not below -> CF=0"""

    label = kwargs['values'][0]
    
    if not FlagRegister.readFlag("CF"):
        return {"next_instruction" : label}

def JB(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if below -> CF=1"""

    label = kwargs['values'][0]
    
    if FlagRegister.readFlag("CF"):
        return {"next_instruction" : label}

def JNAE(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if not above or equal -> CF=1"""

    label = kwargs['values'][0]
    
    if FlagRegister.readFlag("CF"):
        return {"next_instruction" : label}

def JBE(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if below or equal -> CF=1 or ZF=1"""

    label = kwargs['values'][0]

    CF = FlagRegister.readFlag("CF")
    ZF = FlagRegister.readFlag("ZF")
    
    if CF or ZF:
        return {"next_instruction" : label}

def JNA(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if not above -> CF=1 or ZF=1"""

    label = kwargs['values'][0]

    CF = FlagRegister.readFlag("CF")
    ZF = FlagRegister.readFlag("ZF")
    
    if CF or ZF:
        return {"next_instruction" : label}

def JG(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if greater -> SF=0F and ZF=0"""

    label = kwargs['values'][0]

    SF = bool(FlagRegister.readFlag("SF"))
    OF = bool(FlagRegister.readFlag("OF"))
    ZF = FlagRegister.readFlag("ZF")
    
    if SF == OF and ZF == 0:
        return {"next_instruction" : label}

def JNLE(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if not less or equal -> SF=0F and ZF=0"""

    label = kwargs['values'][0]

    SF = bool(FlagRegister.readFlag("SF"))
    OF = bool(FlagRegister.readFlag("OF"))
    ZF = FlagRegister.readFlag("ZF")
    
    if SF == OF and ZF == 0:
        return {"next_instruction" : label}

def JGE(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if greater or equal -> SF=0F"""

    label = kwargs['values'][0]

    SF = bool(FlagRegister.readFlag("SF"))
    OF = bool(FlagRegister.readFlag("OF"))
    
    if SF == OF:
        return {"next_instruction" : label}

def JNL(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if not less -> SF=0F"""

    label = kwargs['values'][0]

    SF = bool(FlagRegister.readFlag("SF"))
    OF = bool(FlagRegister.readFlag("OF"))
    
    if SF == OF:
        return {"next_instruction" : label}

def JL(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if less -> SF<=0F"""

    label = kwargs['values'][0]

    SF = bool(FlagRegister.readFlag("SF"))
    OF = bool(FlagRegister.readFlag("OF"))
    
    if SF <= OF:
        return {"next_instruction" : label}

def JNGE(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if not greater or equal -> SF<=0F"""

    label = kwargs['values'][0]

    SF = bool(FlagRegister.readFlag("SF"))
    OF = bool(FlagRegister.readFlag("OF"))
    
    if SF <= OF:
        return {"next_instruction" : label}

def JLE(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if less or equal -> SF<=0F and ZF=1"""

    label = kwargs['values'][0]

    SF = bool(FlagRegister.readFlag("SF"))
    OF = bool(FlagRegister.readFlag("OF"))
    ZF = FlagRegister.readFlag("ZF")
    
    if SF <= OF and ZF:
        return {"next_instruction" : label}

def JNG(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if not greater -> SF<=0F and ZF=1"""

    label = kwargs['values'][0]

    SF = bool(FlagRegister.readFlag("SF"))
    OF = bool(FlagRegister.readFlag("OF"))
    ZF = FlagRegister.readFlag("ZF")
    
    if SF <= OF and ZF:
        return {"next_instruction" : label}

def JS(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if sign flag is active -> SF=1"""

    label = kwargs['values'][0]

    if FlagRegister.readFlag("SF"):
        return {"next_instruction" : label}

def JNS(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if sign flag is inactive -> SF=0"""

    label = kwargs['values'][0]

    if not FlagRegister.readFlag("SF"):
        return {"next_instruction" : label}

def JC(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if carry flag is active -> CF=1"""

    label = kwargs['values'][0]

    if FlagRegister.readFlag("CF"):
        return {"next_instruction" : label}

def JNC(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if carry flag is inactive -> CF=0"""

    label = kwargs['values'][0]

    if not FlagRegister.readFlag("CF"):
        return {"next_instruction" : label}

def JP(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if parity flag is active -> PF=1"""

    label = kwargs['values'][0]

    if FlagRegister.readFlag("PF"):
        return {"next_instruction" : label}

def JPE(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if parity even -> PF=1"""

    label = kwargs['values'][0]

    if FlagRegister.readFlag("PF"):
        return {"next_instruction" : label}

def JNP(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if parity flag is inactive -> PF=0"""

    label = kwargs['values'][0]

    if not FlagRegister.readFlag("PF"):
        return {"next_instruction" : label}

def JPO(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if parity is odd -> PF=0"""

    label = kwargs['values'][0]

    if not FlagRegister.readFlag("PF"):
        return {"next_instruction" : label}

def JO(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if overflow occured -> OF=1"""

    label = kwargs['values'][0]

    if FlagRegister.readFlag("OF"):
        return {"next_instruction" : label}

def JNO(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if overflow haven't occured -> PF=0"""

    label = kwargs['values'][0]

    if not FlagRegister.readFlag("OF"):
        return {"next_instruction" : label}

def JCXZ(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Jump if value in CX is not 0"""

    label = kwargs['values'][0]

    cx_value = HardwareRegister.readFromRegister("CX")
    cx_int = convert_number_to_int_with_binary_capacity(cx_value, 16)

    if cx_int != 0:
        return {"next_instruction" : label}

################################################################################
#   FUNCTION ATTRIBUTES
################################################################################

# Assign all functions the same attributes - avoid hidious duplication
for fn_name in list(filter(lambda n: n.upper() == n, dir())):
    fn = locals()[fn_name]
    fn.params_range = [1]
    fn.allowed_params_combinations = [(8,)]
