"""
This file contains operations which perform locical operations
"""

from program_code.hardware_registers import HardwareRegisters
from program_code.flag_register import FlagRegister
from program_code.hardware_memory import DataSegment
from program_code.errors import ExecutionOfOperationInLineError, IncorrectParamForBitMovError
from program_code.helper_functions import (convert_number_to_bit_list,
                              save_value_in_destination,
                              eval_no_of_1)

def SHL(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : DataSegment,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """SHIFT LOGICAL LEFT"""

    if kwargs['param_types'][1] == "register" and kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

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
                             kwargs['param_types'][0], kwargs['destination'])

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
        Data : DataSegment,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """SHIFT LOGICAL RIGHT"""

    if kwargs['param_types'][1] == "register" and kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

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
                             kwargs['param_types'][0], kwargs['destination'])

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
        Data : DataSegment,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """SHIFT ARITHMETIC LEFT"""

    if kwargs['param_types'][1] == "register" and kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

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
                             kwargs['param_types'][0], kwargs['destination'])

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
        Data : DataSegment,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """SHIFT ARITHMETIC RIGHT"""

    if kwargs['param_types'][1] == "register" and kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

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
                             kwargs['param_types'][0], kwargs['destination'])

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
        Data : DataSegment,
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

    if kwargs['param_types'][1] == "register" and kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

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
                             kwargs['param_types'][0], kwargs['destination'])

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

def ROR(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : DataSegment,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """ROTATE RIGHT
    
    EX.
    - ROR AL, 3 (AL = 10110001):
        1. 11011000 CL = 1  OF = 0
        2. 01101100 CL = 0  OF = 1
        3. 00110110 CL = 0  OF = 0
    - ROR AL, 1 (AL = 10101101):
        1. 11010110 CL = 1  OF = 0
    """

    if kwargs['param_types'][1] == "register" and kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

    final_size = kwargs['final_size']

    value_to_shift = convert_number_to_bit_list(kwargs['args_values_raw'][0], final_size)
    rotation_counter = kwargs['args_values_int'][1] % final_size

    carry = "0"
    
    for shift in range(rotation_counter):
        value_to_shift.insert(0, value_to_shift[-1])
        carry = value_to_shift[-1]
        overfolow = value_to_shift[0] != value_to_shift[1]
        value_to_shift = value_to_shift[:-1]

    backup_flags = FlagRegister.readFlags()

    FlagRegister.setFlag("OF", overfolow)
    FlagRegister.setFlag("CF", carry == "1")

    new_flags = FlagRegister.readFlags()

    m = save_value_in_destination(HardwareRegister, Data, Variables, value_to_shift,
                             kwargs['param_types'][0], kwargs['destination'])

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

def RCL(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : DataSegment,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """ROTATE THROUGH CARRY LEFT

    Perform rotation as if carry flag was an additional, most significant bit of number

    CF   +    f e d c b a 9 8 7 6 5 4 3 2 1 0

    0    +    0 0 0 0 0 0 0 1 1 1 0 1 0 1 1 1

    After one rotation bit form last position is moved into CF, previous value of CF is moved
    into 'f' and each other bit is shifte one right

    CF   +    f e d c b a 9 8 7 6 5 4 3 2 1 0

    1    +    0 0 0 0 0 0 0 0 1 1 1 0 1 0 1 1
    
    EX.
    - RCL AL, 3 (AL = 00011111 , CL = 1):
        1. 00111111 CL = 0  OF = 0
        2. 01111110 CL = 0  OF = 0
        3. 11111100 CL = 0  OF = 1
    - RCL AL, 1 (AL = 10101101, CL = 0):
        1. 01011010 CL = 1  OF = 1
    """

    if kwargs['param_types'][1] == "register" and kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

    final_size = kwargs['final_size']

    value_to_shift = convert_number_to_bit_list(kwargs['args_values_raw'][0], final_size)
    rotation_counter = kwargs['args_values_int'][1] % final_size

    carry = HardwareRegister.readFromRegister("CF")
    
    for shift in range(rotation_counter):
        value_to_shift.append(carry)
        carry = value_to_shift[0]
        overfolow = value_to_shift[0] != value_to_shift[1]
        value_to_shift = value_to_shift[1:]

    backup_flags = FlagRegister.readFlags()

    FlagRegister.setFlag("OF", overfolow)
    FlagRegister.setFlag("CF", carry == "1")

    new_flags = FlagRegister.readFlags()

    m = save_value_in_destination(HardwareRegister, Data, Variables, value_to_shift,
                             kwargs['param_types'][0], kwargs['destination'])

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

def RCR(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : DataSegment,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """ROTATE THROUGH CARRY RIGH

    Perform rotation as if carry flag was an additional, least significant bit of number
    
    f e d c b a 9 8 7 6 5 4 3 2 1 0   +   CF

    1 0 1 0 1 1 1 0 1 0 1 0 1 0 1 0   +   1

    after one rotation bit from 'f' is moved into 'e', bit from '0' to CF, and previous value
    of 'CF' is moved into 'f'

    f e d c b a 9 8 7 6 5 4 3 2 1 0   +   CF
    
    1 1 0 1 0 1 1 1 0 1 0 1 0 1 0 1   +   0
    
    EX.
    - RCR AL, 3 (AL = 00011111 , CL = 1):
        1. 10001111 CL = 1  OF = 1
        2. 11000111 CL = 1  OF = 0
        3. 11100011 CL = 1  OF = 0
    - RCL AL, 1 (AL = 11111111, CL = 0):
        1. 01111111 CL = 1  OF = 1
    """

    if kwargs['param_types'][1] == "register" and kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

    final_size = kwargs['final_size']

    value_to_shift = convert_number_to_bit_list(kwargs['args_values_raw'][0], final_size)
    rotation_counter = kwargs['args_values_int'][1] % final_size

    carry = HardwareRegister.readFromRegister("CF")
    
    for shift in range(rotation_counter):
        value_to_shift.insert(0, carry)
        carry = value_to_shift[-1]
        overfolow = value_to_shift[0] != value_to_shift[1]
        value_to_shift = value_to_shift[:-1]

    backup_flags = FlagRegister.readFlags()

    FlagRegister.setFlag("OF", overfolow)
    FlagRegister.setFlag("CF", carry == "1")

    new_flags = FlagRegister.readFlags()

    m = save_value_in_destination(HardwareRegister, Data, Variables, value_to_shift,
                             kwargs['param_types'][0], kwargs['destination'])

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

for fn in [SAL, SAR, SHL, SHR, ROL, ROR, RCL, RCR]:
    """Assign all functions the same attributes"""
    fn.params_range = [2]
    fn.allowed_params_combinations = [
        ("memory", "value"), ("memory", "register"), ("register", "value"), 
        ("register", "register") ]
