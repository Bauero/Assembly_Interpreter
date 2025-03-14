"""
This file contains instructions which are responsible for data movement, and does not
change flags, nor perform any operations on stack
"""

from program_code.helper_functions import convert_number_to_bit_list, save_value_in_destination

def MOV(**kwargs):
    """
    # MOVE
    ## Description
    This function copies values from the source to the destination. It doesn't change
    any flag, nor modify the source.
    """
    
    HR  = kwargs["HR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    v = kwargs['args_values_int'][1]
    
    output = list(convert_number_to_bit_list(v, FS))
    m = save_value_in_destination(HR, DS, output, PT, DST)
    
    all_changes = {
        m[0] : [ m[1] ]
        }
    
    return all_changes

def XCHG(**kwargs):
    """
    # EXCHANGE
    ## Description
    This function swaps values between source and destination. It doesn't change any flags.
    """
    
    HR  = kwargs["HR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]

    values_in_binary = [convert_number_to_bit_list(v, FS) for v in RAW]
    save_in_des, save_in_sour = list(values_in_binary[1]), list(values_in_binary[0])

    m1 = save_value_in_destination(HR, DS, save_in_des, PT, DST)
    m2 = save_value_in_destination(HR, DS, save_in_sour, PT, DST)
    
    if m1[0] == m2[0]:
        all_changes = {
            m1[0] : [ m1[1], m2[1] ]
        }
    else:
        all_changes = {
            m1[0] : [ m1[0] ],
            m2[0] : [ m2[0] ],
        } 
    
    return all_changes

#
#   Assign params range and allowed params combination for funcitons
#

MOV.params_range = [2]
MOV.allowed_params_combinations = [
    ("memory", "value"), ("memory", "register"), ("register", "register"), 
    ("register", "value"), ("register", "memory")
]

XCHG.params_range = [2]
XCHG.allowed_params_combinations = [
    ("memory", "register"), ("register", "register"), ("register", "memory")
]
