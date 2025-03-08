"""
This file contains operations which perform locical operations
"""

from program_code.errors import ExecutionOfOperationInLineError, IncorrectParamForBitMovError
from program_code.helper_functions import (convert_number_to_bit_list,
                                           save_value_in_destination,
                                           eval_no_of_1)

def SHL(**kwargs):
    """SHIFT LOGICAL LEFT"""

    if kwargs['param_types'][1] == "register" and \
        kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    value_to_shift = convert_number_to_bit_list(RAW, FS)
    rotation_counter = INT % FS

    first_bit = value_to_shift[0] == "1"
    carry = "0"
    sign = first_bit
    
    for shift in range(rotation_counter):
        value_to_shift.append("0")
        carry = value_to_shift[0]
        sign = value_to_shift[1]
        value_to_shift = value_to_shift[1:]

    first_bit_after = value_to_shift[0] == "1"

    backup_flags = FR.readFlags()

    FR.setFlag("OF", first_bit != first_bit_after)
    FR.setFlag("SF", sign == "1")
    FR.setFlag("CF", carry == "1")
    FR.setFlag("ZF", not "1" in value_to_shift)
    FR.setFlag("PF", eval_no_of_1(value_to_shift))

    new_flags = FR.readFlags()
    m = save_value_in_destination(HR, DS, VAR, value_to_shift, PT, DST)

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

def SHR(**kwargs):
    """SHIFT LOGICAL RIGHT"""

    if kwargs['param_types'][1] == "register" and \
        kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    value_to_shift = convert_number_to_bit_list(RAW, FS)
    rotation_counter = INT % FS

    first_bit = value_to_shift[0] == "1"
    carry = "0"
    sign = first_bit
    
    for shift in range(rotation_counter):
        value_to_shift.insert(0, "0")
        carry = value_to_shift[-1]
        sign = value_to_shift[0]
        value_to_shift = value_to_shift[:-1]

    first_bit_after = value_to_shift[0] == "1"

    backup_flags = FR.readFlags()

    FR.setFlag("OF", first_bit != first_bit_after)
    FR.setFlag("SF", sign == "1")
    FR.setFlag("CF", carry == "1")
    FR.setFlag("ZF", not "1" in value_to_shift)
    FR.setFlag("PF", eval_no_of_1(value_to_shift))

    new_flags = FR.readFlags()
    m = save_value_in_destination(HR, DS, VAR, value_to_shift, PT, DST)

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

def SAL(**kwargs):
    """SHIFT ARITHMETIC LEFT"""

    if kwargs['param_types'][1] == "register" and \
        kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    value_to_shift = convert_number_to_bit_list(RAW, FS)
    rotation_counter = INT % FS

    first_bit = value_to_shift[0] == "1"
    carry = "0"
    sign = first_bit
    
    for shift in range(rotation_counter):
        value_to_shift.append("0")
        carry = value_to_shift[0]
        sign = value_to_shift[1]
        value_to_shift = value_to_shift[1:]

    first_bit_after = value_to_shift[0] == "1"

    backup_flags = FR.readFlags()

    FR.setFlag("OF", first_bit != first_bit_after)
    FR.setFlag("SF", sign == "1")
    FR.setFlag("CF", carry == "1")
    FR.setFlag("ZF", not "1" in value_to_shift)
    FR.setFlag("PF", eval_no_of_1(value_to_shift))

    new_flags = FR.readFlags()
    m = save_value_in_destination(HR, DS, VAR, value_to_shift, PT, DST)

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

def SAR(**kwargs):
    """SHIFT ARITHMETIC RIGHT"""

    if kwargs['param_types'][1] == "register" and \
        kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    value_to_shift = convert_number_to_bit_list(RAW, FS)
    rotation_counter = INT % FS

    first_bit = value_to_shift[0] == "1"
    carry = "0"
    sign = first_bit
    
    for shift in range(rotation_counter):
        value_to_shift.insert(1, value_to_shift[0])
        carry = value_to_shift[-1]
        value_to_shift = value_to_shift[:-1]

    first_bit_after = value_to_shift[0] == "1"

    backup_flags = FR.readFlags()

    FR.setFlag("OF", first_bit != first_bit_after)
    FR.setFlag("SF", sign == "1")
    FR.setFlag("CF", carry == "1")
    FR.setFlag("ZF", not "1" in value_to_shift)
    FR.setFlag("PF", eval_no_of_1(value_to_shift))

    new_flags = FR.readFlags()
    m = save_value_in_destination(HR, DS, VAR, value_to_shift, PT, DST)

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

def ROL(**kwargs):
    """ROTATE LEFT
    
    EX.
    - ROL AL, 3 (AL = 10010000):
        1. 00100001 CL = 1  OF = 1
        2. 01000010 CL = 0  OF = 0
        3. 10000100 CL = 0  OF = 1
    - ROL AL, 1 (AL = 10101101):
        1. 01011011 CL = 1  OF = 1
    """

    if kwargs['param_types'][1] == "register" and \
        kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    value_to_shift = convert_number_to_bit_list(RAW, FS)
    rotation_counter = INT % FS

    carry = "0"
    
    for shift in range(rotation_counter):
        value_to_shift.append(value_to_shift[0])
        carry = value_to_shift[0]
        overfolow = value_to_shift[0] != value_to_shift[1]
        value_to_shift = value_to_shift[1:]

    backup_flags = FR.readFlags()

    FR.setFlag("OF", overfolow)
    FR.setFlag("CF", carry == "1")

    new_flags = FR.readFlags()
    m = save_value_in_destination(HR, DS, VAR, value_to_shift, PT, DST)

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

def ROR(**kwargs):
    """ROTATE RIGHT
    
    EX.
    - ROR AL, 3 (AL = 10110001):
        1. 11011000 CL = 1  OF = 0
        2. 01101100 CL = 0  OF = 1
        3. 00110110 CL = 0  OF = 0
    - ROR AL, 1 (AL = 10101101):
        1. 11010110 CL = 1  OF = 0
    """

    if kwargs['param_types'][1] == "register" and \
        kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    value_to_shift = convert_number_to_bit_list(RAW, FS)
    rotation_counter = INT % FS

    carry = "0"
    
    for shift in range(rotation_counter):
        value_to_shift.insert(0, value_to_shift[-1])
        carry = value_to_shift[-1]
        overfolow = value_to_shift[0] != value_to_shift[1]
        value_to_shift = value_to_shift[:-1]

    backup_flags = FR.readFlags()

    FR.setFlag("OF", overfolow)
    FR.setFlag("CF", carry == "1")

    new_flags = FR.readFlags()
    m = save_value_in_destination(HR, DS, VAR, value_to_shift, PT, DST)

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

def RCL(**kwargs):
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

    if kwargs['param_types'][1] == "register" and \
        kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    value_to_shift = convert_number_to_bit_list(RAW, FS)
    rotation_counter = INT % FS

    carry = HR.readFromRegister("CF")
    
    for shift in range(rotation_counter):
        value_to_shift.append(carry)
        carry = value_to_shift[0]
        overfolow = value_to_shift[0] != value_to_shift[1]
        value_to_shift = value_to_shift[1:]

    backup_flags = FR.readFlags()

    FR.setFlag("OF", overfolow)
    FR.setFlag("CF", carry == "1")

    new_flags = FR.readFlags()
    m = save_value_in_destination(HR, DS, VAR, value_to_shift, PT, DST)

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

def RCR(**kwargs):
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

    if kwargs['param_types'][1] == "register" and \
        kwargs['source_params'][1].upper() != "CL":
        raise ExecutionOfOperationInLineError(
            IncorrectParamForBitMovError()
        )

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    value_to_shift = convert_number_to_bit_list(RAW, FS)
    rotation_counter = INT % FS

    carry = HR.readFromRegister("CF")
    
    for shift in range(rotation_counter):
        value_to_shift.insert(0, carry)
        carry = value_to_shift[-1]
        overfolow = value_to_shift[0] != value_to_shift[1]
        value_to_shift = value_to_shift[:-1]

    backup_flags = FR.readFlags()

    FR.setFlag("OF", overfolow)
    FR.setFlag("CF", carry == "1")

    new_flags = FR.readFlags()
    m = save_value_in_destination(HR, DS, VAR, value_to_shift, PT, DST)

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
