"""
This file contains operations which perform locical operations
"""

from hardware_registers import HardwareRegisters
from flag_register import FlagRegister
from datatypes import Data
from helper_functions import (convert_number_to_bit_list,
                              save_value_in_destination,
                              eval_no_of_1)

def SHL(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """SHIFT LOGICAL LEFT"""

    final_size = kwargs['final_size']

    value_to_shift = convert_number_to_bit_list(kwargs['args_values_raw'][0], final_size)
    rotation_counter = kwargs['args_values_int'][1] % final_size

    first_bit = value_to_shift[0] == "1"
    carry = "0"
    sign = first_bit
    
    for shift in range(rotation_counter):
        value_to_shift.append("0")
        carry = value_to_shift[0]
        sign = value_to_shift[1]
        value_to_shift = value_to_shift[1:]

    first_bit_after = value_to_shift[0] == "1"

    backup_flags = FlagRegister.readFlags()

    FlagRegister.setFlag("OF", first_bit != first_bit_after)
    FlagRegister.setFlag("SF", sign == "1")
    FlagRegister.setFlag("CF", carry == "1")
    FlagRegister.setFlag("ZF", not "1" in value_to_shift)
    FlagRegister.setFlag("PF", eval_no_of_1(value_to_shift))

    new_flags = FlagRegister.readFlags()

    m = save_value_in_destination(HardwareRegister, Data, Variables, value_to_shift,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    all_changes = {
        m[0] : [
            m[1]
        ],
        "flags" : {
            "oryginal_value" :  backup_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def SHR(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """SHIFT LOGICAL RIGHT"""

    final_size = kwargs['final_size']

    value_to_shift = convert_number_to_bit_list(kwargs['args_values_raw'][0], final_size)
    rotation_counter = kwargs['args_values_int'][1] % final_size

    first_bit = value_to_shift[0] == "1"
    carry = "0"
    sign = first_bit
    
    for shift in range(rotation_counter):
        value_to_shift.insert(0, "0")
        carry = value_to_shift[-1]
        sign = value_to_shift[0]
        value_to_shift = value_to_shift[:-1]

    first_bit_after = value_to_shift[0] == "1"

    backup_flags = FlagRegister.readFlags()

    FlagRegister.setFlag("OF", first_bit != first_bit_after)
    FlagRegister.setFlag("SF", sign == "1")
    FlagRegister.setFlag("CF", carry == "1")
    FlagRegister.setFlag("ZF", not "1" in value_to_shift)
    FlagRegister.setFlag("PF", eval_no_of_1(value_to_shift))

    new_flags = FlagRegister.readFlags()

    m = save_value_in_destination(HardwareRegister, Data, Variables, value_to_shift,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    all_changes = {
        m[0] : [
            m[1]
        ],
        "flags" : {
            "oryginal_value" :  backup_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def SAL(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """SHIFT ARITHMETIC LEFT"""

    final_size = kwargs['final_size']

    value_to_shift = convert_number_to_bit_list(kwargs['args_values_raw'][0], final_size)
    rotation_counter = kwargs['args_values_int'][1] % final_size

    first_bit = value_to_shift[0] == "1"
    carry = "0"
    sign = first_bit
    
    for shift in range(rotation_counter):
        value_to_shift.append("0")
        carry = value_to_shift[0]
        sign = value_to_shift[1]
        value_to_shift = value_to_shift[1:]

    first_bit_after = value_to_shift[0] == "1"

    backup_flags = FlagRegister.readFlags()

    FlagRegister.setFlag("OF", first_bit != first_bit_after)
    FlagRegister.setFlag("SF", sign == "1")
    FlagRegister.setFlag("CF", carry == "1")
    FlagRegister.setFlag("ZF", not "1" in value_to_shift)
    FlagRegister.setFlag("PF", eval_no_of_1(value_to_shift))

    new_flags = FlagRegister.readFlags()

    m = save_value_in_destination(HardwareRegister, Data, Variables, value_to_shift,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    all_changes = {
        m[0] : [
            m[1]
        ],
        "flags" : {
            "oryginal_value" :  backup_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def SAR(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """SHIFT ARITHMETIC RIGHT"""

    final_size = kwargs['final_size']

    value_to_shift = convert_number_to_bit_list(kwargs['args_values_raw'][0], final_size)
    rotation_counter = kwargs['args_values_int'][1] % final_size

    first_bit = value_to_shift[0] == "1"
    carry = "0"
    sign = first_bit
    
    for shift in range(rotation_counter):
        value_to_shift.insert(1, value_to_shift[0])
        carry = value_to_shift[-1]
        value_to_shift = value_to_shift[:-1]

    first_bit_after = value_to_shift[0] == "1"

    backup_flags = FlagRegister.readFlags()

    FlagRegister.setFlag("OF", first_bit != first_bit_after)
    FlagRegister.setFlag("SF", sign == "1")
    FlagRegister.setFlag("CF", carry == "1")
    FlagRegister.setFlag("ZF", not "1" in value_to_shift)
    FlagRegister.setFlag("PF", eval_no_of_1(value_to_shift))

    new_flags = FlagRegister.readFlags()

    m = save_value_in_destination(HardwareRegister, Data, Variables, value_to_shift,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    all_changes = {
        m[0] : [
            m[1]
        ],
        "flags" : {
            "oryginal_value" :  backup_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def ROL(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """ROTATE LEFT
    
    EX.
    - ROL AL, 3 (AL = 10010000):
        1. 00100001 CL = 1  OF = 1
        2. 01000010 CL = 0  OF = 0
        3. 10000100 CL = 0  OF = 1
    - ROL AL, 1 (AL = 10101101):
        1. 01011011 CL = 1  OF = 1
    """

    final_size = kwargs['final_size']

    value_to_shift = convert_number_to_bit_list(kwargs['args_values_raw'][0], final_size)
    rotation_counter = kwargs['args_values_int'][1] % final_size

    carry = "0"
    
    for shift in range(rotation_counter):
        value_to_shift.append(value_to_shift[0])
        carry = value_to_shift[0]
        overfolow = value_to_shift[0] != value_to_shift[1]
        value_to_shift = value_to_shift[1:]

    backup_flags = FlagRegister.readFlags()

    FlagRegister.setFlag("OF", overfolow)
    FlagRegister.setFlag("CF", carry == "1")

    new_flags = FlagRegister.readFlags()

    m = save_value_in_destination(HardwareRegister, Data, Variables, value_to_shift,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    all_changes = {
        m[0] : [
            m[1]
        ],
        "flags" : {
            "oryginal_value" :  backup_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

for fn in [SAL, SAR, SHL, SHR, ROL]:
    """Assign all functions the same attributes"""
    fn.params_range = [2]
    fn.allowed_params_combinations = [ ("memory", "value"), ("register", "value")]
