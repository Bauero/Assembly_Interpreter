"""
This file contains operations which perform locical operations
"""

from program_code.hardware_registers import HardwareRegisters
from program_code.flag_register import FlagRegister
from program_code.hardware_memory import DataSegment
from program_code.helper_functions import (save_value_in_destination,
                              convert_number_to_bit_list,
                              eval_no_of_1)

def AND(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : DataSegment,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Performs logical and operation on two numbers"""

    final_size = kwargs['final_size']
    values_in_int = kwargs["args_values_int"]

    and_value = values_in_int[0] ^ values_in_int[1]
    output = convert_number_to_bit_list(and_value, final_size).zfill(final_size)
    output = output[-final_size:]   # {final_size} bits from the end

    previous_flags = list(FlagRegister.readFlags())

    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", 0)
    FlagRegister.setFlag("PF", eval_no_of_1(output))
    FlagRegister.setFlag("OF", 0)
    
    new_flags = list(FlagRegister.readFlags())

    m = save_value_in_destination(HardwareRegister, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['destination'])

    all_changes = {
        m[0] : [m[1]],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def OR(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : DataSegment,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Performs logical and operation on two numbers"""

    final_size = kwargs['final_size']

    # Convert both numbers to be in raw binary form -> 0111010110101101
    values_in_binary = []
    
    for v in kwargs['args_values_raw']:
        output = convert_number_to_bit_list(v, final_size)
        values_in_binary.append(output)
        
    # Perform binary or operation
    output = []
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        result = str(int(b1 or b2))
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
    FlagRegister.setFlag("PF", eval_no_of_1(output))
    FlagRegister.setFlag("OF", 0)
    
    new_flags = list(FlagRegister.readFlags())

    m = save_value_in_destination(HardwareRegister, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['destination'])

    all_changes = {
        m[0] : [m[1]],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def XOR(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : DataSegment,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Performs logical and operation on two numbers"""

    final_size = kwargs['final_size']

    # Convert both numbers to be in raw binary form -> 0111010110101101
    values_in_binary = []
    
    for v in kwargs['args_values_raw']:
        output = convert_number_to_bit_list(v, final_size)
        values_in_binary.append(output)
        
    # Perform binary xor operation
    output = []
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        result = str(int((b1 or b2) and not (b1 and b2)))
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
    FlagRegister.setFlag("PF", eval_no_of_1(output))
    FlagRegister.setFlag("OF", 0)
    
    new_flags = list(FlagRegister.readFlags())

    m = save_value_in_destination(HardwareRegister, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['destination'])

    all_changes = {
        m[0] : [m[1]],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def NOT(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : DataSegment,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Performs logical and operation on two numbers"""

    final_size = kwargs['final_size']

    # Convert both numbers to be in raw binary form -> 0111010110101101
    values_in_binary = []
    
    for v in kwargs['args_values_raw']:
        output = convert_number_to_bit_list(v, final_size)
        values_in_binary.append(output)
        
    # Perform binary not operation
    output = list(map(lambda x: str(int(not int(x) == 1)), values_in_binary[0]))

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    m = save_value_in_destination(HardwareRegister, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['destination'])

    all_changes = {
        m[0] : [m[1]],
    }

    return all_changes

def NOP(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : DataSegment,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function does nothing - just takes time"""

    return {}

def TEST(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : DataSegment,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Logical compare between elements
    
    Argumen1 ^ Argument2
    """
    final_size = kwargs['final_size']

    values_in_int = kwargs["args_values_int"]

    and_value = values_in_int[0] ^ values_in_int[1]
    output = convert_number_to_bit_list(and_value, final_size).zfill(final_size)
    output = output[-final_size:]

    previous_flags = list(FlagRegister.readFlags())

    FlagRegister.setFlag("ZF", not "1" in output)
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", 0)
    FlagRegister.setFlag("PF", eval_no_of_1(output))
    FlagRegister.setFlag("OF", 0)
    
    new_flags = list(FlagRegister.readFlags())
    
    all_changes = {
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

for fn in [AND, OR, XOR, TEST]:
    """Assign all functions the same attributes"""
    fn.params_range = [2]
    fn.allowed_params_combinations = [
        ("memory", "value"), ("memory", "register"), ("register", "register"), 
        ("register", "value"), ("register", "memory")
    ]

NOT.params_range = [1]
NOT.allowed_params_combinations = [ ("memory",), ("register",) ]

NOP.params_range = [0]
NOP.allowed_params_combinations = [tuple()]
