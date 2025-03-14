"""
This file contains all jump instuctions which are supported in x86 Assembly
"""

from program_code.helper_functions import convert_number_to_int_with_binary_capacity

def JMP(**kwargs):
    """
    # JUMP
    ## Description
    This function performs unconditional jump to label.
    """

    LBL = kwargs['args_values_int'][0]

    return {"next_instruction" : LBL}

def JZ(**kwargs):
    """
    # JUMP IF ZERO
    ## Description
    Jump if last operation was equal zero -> ZF=1.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    
    if FR.readFlag("ZF"):   return {"next_instruction" : LBL}

def JE(**kwargs):
    """
    # JUMP IF EQUAL
    ## Description
    Jump if numbers are equal -> ZF=1.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    
    if FR.readFlag("ZF"):   return {"next_instruction" : LBL}

def JNZ(**kwargs):
    """
    # JUMP IF NOT ZERO
    ## Description
    Jump if last operation wasn't equal to zero -> ZF=0.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    
    if not FR.readFlag("ZF"):   return {"next_instruction" : LBL}

def JNE(**kwargs):
    """
    # JUMP IF NOT EQUAL
    ## Description
    Jump if numbers aren't equal -> ZF=0.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    
    if not FR.readFlag("ZF"):   return {"next_instruction" : LBL}
    if not FR.readFlag("SF"):   return {"next_instruction" : LBL}

def JA(**kwargs):
    """
    # JUMP IF ABOVE
    ## Description
    Jump if last result was above zero -> CF=0 AND ZF=0.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    CF  = FR.readFlag("CF")
    ZF  = FR.readFlag("ZF")
    
    if not (CF or ZF):  return {"next_instruction" : LBL}

def JNBE(**kwargs):
    """
    # JUMP IF NOT BELOW
    ## Description
    Jump if last result not below or equal 0 -> CF=0 AND ZF=0.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    CF  = FR.readFlag("CF")
    ZF  = FR.readFlag("ZF")
    
    if not (CF or ZF):  return {"next_instruction" : LBL}

def JAE(**kwargs):
    """
    # JUMP IF ABOVE OR EQUAL
    ## Description
    Jump if above or equal -> CF=0.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    
    if not FR.readFlag("CF"):   return {"next_instruction" : LBL}

def JNB(**kwargs):
    """
    # JUMP IF NOT BELOW
    ## Description
    Jump if not below -> CF=0.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    
    if not FR.readFlag("CF"):   return {"next_instruction" : LBL}

def JB(**kwargs):
    """
    # JUMP IF BELOW
    ## Description
    Jump if below -> CF=1.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    
    if FR.readFlag("CF"):   return {"next_instruction" : LBL}

def JNAE(**kwargs):
    """
    # JUMP IF NOT ABOVE OR EQUAL
    ## Description
    Jump if not above or equal -> CF=1.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    
    if FR.readFlag("CF"):   return {"next_instruction" : LBL}

def JBE(**kwargs):
    """
    # JUMP IF BELOW OR EQUAL
    ## Description
    Jump if below or equal -> CF=1 or ZF=1.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    CF  = FR.readFlag("CF")
    ZF  = FR.readFlag("ZF")
    
    if CF or ZF:    return {"next_instruction" : LBL}

def JNA(**kwargs):
    """
    # JUMP IF NOT ABOVE
    ## Description
    Jump if not above -> CF=1 or ZF=1.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    CF  = FR.readFlag("CF")
    ZF  = FR.readFlag("ZF")
    
    if CF or ZF:    return {"next_instruction" : LBL}

def JG(**kwargs):
    """
    # JUMP IF GREATER
    ## Description
    Jump if greater -> SF=0F and ZF=0.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    SF  = bool(FR.readFlag("SF"))
    OF  = bool(FR.readFlag("OF"))
    ZF  = FR.readFlag("ZF")
    
    if SF == OF and ZF == 0:    return {"next_instruction" : LBL}

def JNLE(**kwargs):
    """
    # JUMP IF NOT LESS OR EQUAL
    ## Description
    Jump if not less or equal -> SF=0F and ZF=0.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    SF  = bool(FR.readFlag("SF"))
    OF  = bool(FR.readFlag("OF"))
    ZF  = FR.readFlag("ZF")
    
    if SF == OF and ZF == 0:    return {"next_instruction" : LBL}

def JGE(**kwargs):
    """
    # JUMP IF GRETER OR EQUAL
    ## Description
    Jump if greater or equal -> SF=0F.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    SF  = bool(FR.readFlag("SF"))
    OF  = bool(FR.readFlag("OF"))
    
    if SF == OF:    return {"next_instruction" : LBL}

def JNL(**kwargs):
    """
    # JUMP IF NOT LESS
    ## Description
    Jump if not less -> SF=0F.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    SF  = bool(FR.readFlag("SF"))
    OF  = bool(FR.readFlag("OF"))
    
    if SF == OF:    return {"next_instruction" : LBL}

def JL(**kwargs):
    """
    # JUMP LESS
    ## Description
    Jump if less -> SF<=0F.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    SF  = bool(FR.readFlag("SF"))
    OF  = bool(FR.readFlag("OF"))
    
    if SF <= OF:    return {"next_instruction" : LBL}

def JNGE(**kwargs):
    """
    # JUMP IF NOT GREATER OR EQUAL
    ## Description
    Jump if not greater or equal -> SF<=0F.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    SF  = bool(FR.readFlag("SF"))
    OF  = bool(FR.readFlag("OF"))
    
    if SF <= OF:    return {"next_instruction" : LBL}

def JLE(**kwargs):
    """
    # JUMP IF LESS OF EQUAL
    ## Description
    Jump if less or equal -> SF<=0F and ZF=1.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    SF  = bool(FR.readFlag("SF"))
    OF  = bool(FR.readFlag("OF"))
    ZF  = FR.readFlag("ZF")
    
    if SF <= OF and ZF: return {"next_instruction" : LBL}

def JNG(**kwargs):
    """
    # JUMP IF NOT GREATER
    ## Description
    Jump if not greater -> SF<=0F and ZF=1.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]
    SF  = bool(FR.readFlag("SF"))
    OF  = bool(FR.readFlag("OF"))
    ZF  = FR.readFlag("ZF")
    
    if SF <= OF and ZF: return {"next_instruction" : LBL}

def JS(**kwargs):
    """
    # JUMP IF SIGN
    ## Description
    Jump if sign flag is active -> SF=1.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]

    if FR.readFlag("SF"):   return {"next_instruction" : LBL}

def JNS(**kwargs):
    """
    # JUMP IF NOT SIGN
    ## Description
    Jump if sign flag is inactive -> SF=0.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]

    if not FR.readFlag("SF"):   return {"next_instruction" : LBL}

def JC(**kwargs):
    """
    # JUMP IF CARRY
    ## Description
    Jump if carry flag is active -> CF=1.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]

    if FR.readFlag("CF"):   return {"next_instruction" : LBL}

def JNC(**kwargs):
    """
    # JUMP IF NOT CARRY
    ## Description
    Jump if carry flag is inactive -> CF=0.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]

    if not FR.readFlag("CF"):   return {"next_instruction" : LBL}

def JP(**kwargs):
    """
    # JUMP IF PARITY
    ## Description
    Jump if parity flag is active -> PF=1.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]

    if FR.readFlag("PF"):   return {"next_instruction" : LBL}

def JPE(**kwargs):
    """
    # JUMP IF PARITY EVEN
    ## Description
    Jump if parity even -> PF=1.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]

    if FR.readFlag("PF"):   return {"next_instruction" : LBL}

def JNP(**kwargs):
    """
    # JUMP NOT PARITY
    ## Description
    Jump if parity flag is inactive -> PF=0.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]

    if not FR.readFlag("PF"):   return {"next_instruction" : LBL}

def JPO(**kwargs):
    """
    # JUMP PARITY ODD
    ## Description
    Jump if parity is odd -> PF=0.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]

    if not FR.readFlag("PF"):   return {"next_instruction" : LBL}

def JO(**kwargs):
    """
    # JUMP IF OVERFLOW
    ## Description
    Jump if overflow occured -> OF=1.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]

    if FR.readFlag("OF"):   return {"next_instruction" : LBL}

def JNO(**kwargs):
    """
    # JUMP IF NOT OVERFLOW
    ## Description
    Jump if overflow haven't occured -> PF=0.
    """

    FR  = kwargs["FR"]
    LBL = kwargs['args_values_int'][0]

    if not FR.readFlag("OF"):   return {"next_instruction" : LBL}

def JCXZ(**kwargs):
    """
    # JUMP IF CX
    ## Description
    Jump if value in CX is not 0.
    """

    HR  = kwargs["HR"]
    LBL = kwargs['args_values_int'][0]

    cx_value = HR.readFromRegister("CX")
    cx_int = convert_number_to_int_with_binary_capacity(cx_value, 16)

    if cx_int != 0: return {"next_instruction" : LBL}

#
#   Assign params range and allowed params combination for funcitons
#

for fn_name in list(filter(lambda n: n.upper() == n, dir())):
    fn = locals()[fn_name]
    fn.params_range = [1]
    fn.allowed_params_combinations = [("value",), ("label",)]
