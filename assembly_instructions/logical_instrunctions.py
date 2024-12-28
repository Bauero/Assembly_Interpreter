"""
This file contains operations which perform locical operations
"""

from hardware_registers import HardwareRegisters
from flag_register import FlagRegister
from stack import Stack
from datatypes import Data

################################################################################
#   FUNCTION DEFINITIONS
################################################################################

def AND(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Performs logical and operation on two numbers"""

    final_size = kwargs['final_size']

    # Convert both numbers to be in raw binary form -> 0111010110101101
    values_in_binary = []
    
    for v in kwargs['values']:
        if new_val := return_if_base_16_value(v):
            prep_val = bin(int(new_val[2:], base=16))[2:]
        elif new_val := return_if_base_10_value(v):
            prep_val = bin(int(new_val))[2:]
        elif new_val := return_if_base_2_value(v):
            prep_val = new_val[:-1] if new_val.lower().endswith('b') else new_val
        else:
            raise WrongNumberBase(v)
        values_in_binary.append(prep_val.zfill(final_size))
        
    # Perform binary and operation
    output = []
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        result = b1 * b2
        carry = result == 1
        output.insert(0, str(result))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    previous_flags = list(FlagRegister.readFlags())

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", 0)
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", 0)
    
    new_flags = list(FlagRegister.readFlags())

    m = save_value_in_destination(HardwareRegister, Stack, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    all_changes = {
        m[0] : m[1],
        "flags" : {
            "previous_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def OR(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Performs logical and operation on two numbers"""

    final_size = kwargs['final_size']

    # Convert both numbers to be in raw binary form -> 0111010110101101
    values_in_binary = []
    
    for v in kwargs['values']:
        if new_val := return_if_base_16_value(v):
            prep_val = bin(int(new_val[2:], base=16))[2:]
        elif new_val := return_if_base_10_value(v):
            prep_val = bin(int(new_val))[2:]
        elif new_val := return_if_base_2_value(v):
            prep_val = new_val[:-1] if new_val.lower().endswith('b') else new_val
        else:
            raise WrongNumberBase(v)
        values_in_binary.append(prep_val.zfill(final_size))
        
    # Perform binary or operation
    output = []
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        result = b1 or b2
        carry = result == 1
        output.insert(0, str(result))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    previous_flags = list(FlagRegister.readFlags())

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", 0)
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", 0)
    
    new_flags = list(FlagRegister.readFlags())

    m = save_value_in_destination(HardwareRegister, Stack, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    all_changes = {
        m[0] : m[1],
        "flags" : {
            "previous_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def XOR(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Performs logical and operation on two numbers"""

    final_size = kwargs['final_size']

    # Convert both numbers to be in raw binary form -> 0111010110101101
    values_in_binary = []
    
    for v in kwargs['values']:
        if new_val := return_if_base_16_value(v):
            prep_val = bin(int(new_val[2:], base=16))[2:]
        elif new_val := return_if_base_10_value(v):
            prep_val = bin(int(new_val))[2:]
        elif new_val := return_if_base_2_value(v):
            prep_val = new_val[:-1] if new_val.lower().endswith('b') else new_val
        else:
            raise WrongNumberBase(v)
        values_in_binary.append(prep_val.zfill(final_size))
        
    # Perform binary xor operation
    output = []
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        result = (b1 or b2) and not (b1 and b2)
        carry = b1 and b2
        output.insert(0, str(result))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    previous_flags = list(FlagRegister.readFlags())

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", 0)
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", 0)
    
    new_flags = list(FlagRegister.readFlags())

    m = save_value_in_destination(HardwareRegister, Stack, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    all_changes = {
        m[0] : m[1],
        "flags" : {
            "previous_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def NOT(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Performs logical and operation on two numbers"""

    final_size = kwargs['final_size']

    # Convert both numbers to be in raw binary form -> 0111010110101101
    values_in_binary = []
    
    for v in kwargs['values']:
        if new_val := return_if_base_16_value(v):
            prep_val = bin(int(new_val[2:], base=16))[2:]
        elif new_val := return_if_base_10_value(v):
            prep_val = bin(int(new_val))[2:]
        elif new_val := return_if_base_2_value(v):
            prep_val = new_val[:-1] if new_val.lower().endswith('b') else new_val
        else:
            raise WrongNumberBase(v)
        values_in_binary.append(prep_val.zfill(final_size))
        
    # Perform binary not operation
    output = list(map(lambda x: not int(x) == 1, values_in_binary[0]))

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    m = save_value_in_destination(HardwareRegister, Stack, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    all_changes = {
        m[0] : m[1],
    }

    return all_changes

################################################################################
#   FUNCTION ATTRIBUTES
################################################################################

AND.params_range = [2]
AND.allowed_params_combinations = [
    (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
    (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
]

OR.params_range = [2]
OR.allowed_params_combinations = [
    (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
    (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
]

XOR.params_range = [2]
XOR.allowed_params_combinations = [
    (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
    (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
]

NOT.params_range = [1]
NOT.allowed_params_combinations = [ (2,), (3,), (4,), (5,), (6,) ]
