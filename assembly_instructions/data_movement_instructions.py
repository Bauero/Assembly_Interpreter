"""
This file contains instructions which are responsible for data movement, and does not
change flags, nor perform any operations on stack
"""

from hardware_registers import HardwareRegisters
from flag_register import FlagRegister
from stack import Stack
from datatypes import Data
from helper_functions import convert_number_to_bit_list, save_value_in_destination

################################################################################
#   FUNCTION DEFINITIONS
################################################################################

def MOV(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function perfoms movement of data from place to place"""
    
    final_size = kwargs['final_size']
    v = kwargs['values'][1]
    output = list(convert_number_to_bit_list(v, final_size))

    m = save_value_in_destination(HardwareRegister, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])
    
    all_changes = {
        m[0] : [ m[1] ]
        }
    
    return all_changes

def XCHG(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function swaps values between source and destination"""
    
    final_size = kwargs['final_size']
    values_in_binary = []
    
    for v in kwargs['values']:
        output = convert_number_to_bit_list(v, final_size)
        values_in_binary.append(output)
    
    save_in_des, save_in_sour = list(values_in_binary[1]), list(values_in_binary[0])

    m1 = save_value_in_destination(HardwareRegister, Data, Variables, save_in_des,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    m2 = save_value_in_destination(HardwareRegister, Data, Variables, save_in_sour,
                             kwargs['param_types'][0], kwargs['source_params'][0])
    
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

################################################################################
#   FUNCITON ATTRIBUTES
################################################################################

MOV.params_range = [2]
MOV.allowed_params_combinations = [
    (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
    (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
]

XCHG.params_range = [2]
XCHG.allowed_params_combinations = [
    (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
    (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
]
