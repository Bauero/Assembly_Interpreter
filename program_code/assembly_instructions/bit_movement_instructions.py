"""
This file contains operations which perform locical operations
"""

from program_code.helper_functions import (convert_number_to_bit_list,
                                           save_value_in_destination,
                                           eval_no_of_1)

def SHL(**kwargs):
    """
    # SHIFT LOGICAL LEFT
    ## Description
    This operation shifts whole numer to the left. Each shift movest most significant bit
    to CF, removes most siginificant bit from the number, and at the end, as the least 
    significant bit puts 0. Sets all flags except AF, based on the end result.

    ## Summary
    Shift number left, putting previously MSB into CF, filling empty places with 0
    
    ## EX.
    - SHL AL, 1 (AL == 255, CF = ?) -> AL = 254 (11111110), CF = 1
    - SHL AL, CL (AL == 255, CL = 3, CF = ?) -> AL = 248 (11111000), CF = 1
    - SHL AL, CL (AL == 1, CL = 3, CF = ?) -> AL = 8 (00001000), CF = 0
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types']
    SOP = kwargs["source_params"]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    if PT[1] == "register" and SOP[1].upper() != "CL":
        return {"error" : {
            "popup" : "incorrect_param_bit_movement",
            "line" : kwargs["line"] + 1,
            "source_error" : None
        }}

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
    m = save_value_in_destination(HR, DS, value_to_shift, PT[0], DST)

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
    """
    # SHIFT LOGICAL RIGHT
    ## Description
    This operation shifts whole numer to the right. Each shift movest least significant bit
    to CF, removes most siginificant bit from the number, in place of the most signivicant
    bit puts 0. Sets all flags except AF, based on the end result.

    ## Summary
    Shift number right, putting previously LSB into CF, filling empty places with 0
    
    ## EX.
    - SHR AL, 1 (AL == 255, CF = ?) -> AL = 127 (01111111), CF = 1
    - SHR AL, CL (AL == 255, CL = 3, CF = ?) -> AL = 31 (00011111), CF = 1
    - SHR AL, CL (AL == 100, CL = 3, CF = ?) -> AL = 12 (00001100), CF = 1
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types']
    SOP = kwargs["source_params"]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    if PT[1] == "register" and SOP[1].upper() != "CL":
        return {"error" : {
            "popup" : "incorrect_param_bit_movement",
            "line" : kwargs["line"] + 1,
            "source_error" : None
        }}

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
    m = save_value_in_destination(HR, DS, value_to_shift, PT[0], DST)

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
    """
    # SHIFT ARITHMETIC LEFT
    ## Description
    This operation shifts whole numer to the left. Each shift movest most significant bit
    to CF, removes most siginificant bit from the number, and at the end, as the least 
    significant bit puts 0. Sets all flags except AF, based on the end result.

    ## Summary
    Shift number left, putting previously MSB into CF, filling empty places with 0
    
    ## EX.
    - SAL AL, 1 (AL == 255, CF = ?) -> AL = 254 (11111110), CF = 1
    - SAL AL, CL (AL == 255, CL = 3, CF = ?) -> AL = 248 (11111000), CF = 1
    - SAL AL, CL (AL == 1, CL = 3, CF = ?) -> AL = 8 (00001000), CF = 0
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types']
    SOP = kwargs["source_params"]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    if PT[1] == "register" and SOP[1].upper() != "CL":
        return {"error" : {
            "popup" : "incorrect_param_bit_movement",
            "line" : kwargs["line"] + 1,
            "source_error" : None
        }}

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
    m = save_value_in_destination(HR, DS, value_to_shift, PT[0], DST)

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
    """
    # SHIFT ARITHMETIC RIGHT
    ## Description
    This operation shifts whole numer (except most significant bit) to the right.
    Least significant bit is moved to CF, while in place of second most significant
    bit 0 is placed. Affects all flags except AF.

    ## Summary
    Shift number right except most significant bit
    
    ## EX.
    - SAR AL, 1 (AL == 255, CF = ?) -> AL = 191 (10111111), CF = 1
    - SAR AL, CL (AL == 255, CL = 3, CF = ?) -> AL = 143 (10001111), CF = 1
    - SAR AL, CL (AL == 100, CL = 3, CF = ?) -> AL = 12 (00001100), CF = 1
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types']
    SOP = kwargs["source_params"]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    if PT[1] == "register" and SOP[1].upper() != "CL":
        return {"error" : {
            "popup" : "incorrect_param_bit_movement",
            "line" : kwargs["line"] + 1,
            "source_error" : None
        }}

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
    m = save_value_in_destination(HR, DS, value_to_shift, PT[0], DST)

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
    """
    # ROTATE LEFT
    ## Description
    Rotates bits of number as on carousel, storing value of last moved bit in CF,
    and setting OF if after rotation bit on the first place is different than before
    rotation. Sets only CF and OF.

    ## Summary
    Shift bit left, but instead of filling with 0 on the right, fill with value which
    was MSB before shift

    ## EX.
    - ROL AL, CL (AL = 10010000, CL = 3):
        1. 00100001 CL = 1  OF = 1
        2. 01000010 CL = 0  OF = 0
        3. 10000100 CL = 0  OF = 1
    - ROL AL, 1 (AL = 10101101):
        1. 01011011 CL = 1  OF = 1
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types']
    SOP = kwargs["source_params"]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    if PT[1] == "register" and SOP[1].upper() != "CL":
        return {"error" : {
            "popup" : "incorrect_param_bit_movement",
            "line" : kwargs["line"] + 1,
            "source_error" : None
        }}

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
    m = save_value_in_destination(HR, DS, value_to_shift, PT[0], DST)

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
    """
    # ROTATE RIGHT
    ## Description
    Rotates bits of number as on carousel, storing value of last moved bit in CF,
    and setting OF if after rotation bit on the first place is different than before
    rotation. Sets only CF and OF.

    ## Summary
    Shift bit right, but instead of filling with 0 on the right, fill with value which
    was LSB before shift
    
    EX.
    - ROR AL, CL (AL = 10110001, CL = 3):
        1. 11011000 CL = 1  OF = 0
        2. 01101100 CL = 0  OF = 1
        3. 00110110 CL = 0  OF = 0
    - ROR AL, 1 (AL = 10101101):
        1. 11010110 CL = 1  OF = 0
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types']
    SOP = kwargs["source_params"]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    if PT[1] == "register" and SOP[1].upper() != "CL":
        return {"error" : {
            "popup" : "incorrect_param_bit_movement",
            "line" : kwargs["line"] + 1,
            "source_error" : None
        }}

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
    m = save_value_in_destination(HR, DS, value_to_shift, PT[0], DST)

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
    """
    # ROTATE THROUGH CARRY LEFT
    ## Description
    Perform rotation as if carry flag was an additional, most significant bit of number
    ```
    CF   +    f e d c b a 9 8 7 6 5 4 3 2 1 0

    0    +    0 0 0 0 0 0 0 1 1 1 0 1 0 1 1 1
    ```
    After one rotation bit form last position is moved into CF, previous value of CF is moved
    into 'f' and each other bit is shifte one right
    ```
    CF   +    f e d c b a 9 8 7 6 5 4 3 2 1 0

    1    +    0 0 0 0 0 0 0 0 1 1 1 0 1 0 1 1
    ```
    ## EX.
    - RCL AL, 3 (AL = 00011111 , CL = 1):
        1. 00111111 CL = 0  OF = 0
        2. 01111110 CL = 0  OF = 0
        3. 11111100 CL = 0  OF = 1
    - RCL AL, 1 (AL = 10101101, CL = 0):
        1. 01011010 CL = 1  OF = 1
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types']
    SOP = kwargs["source_params"]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    if PT[1] == "register" and SOP[1].upper() != "CL":
        return {"error" : {
            "popup" : "incorrect_param_bit_movement",
            "line" : kwargs["line"] + 1,
            "source_error" : None
        }}

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
    m = save_value_in_destination(HR, DS, value_to_shift, PT[0], DST)

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
    """
    # ROTATE THROUGH CARRY RIGH
    ## Description
    Perform rotation as if carry flag was an additional, least significant bit of number
    ```
    f e d c b a 9 8 7 6 5 4 3 2 1 0   +   CF

    1 0 1 0 1 1 1 0 1 0 1 0 1 0 1 0   +   1
    ```
    after one rotation bit from 'f' is moved into 'e', bit from '0' to CF, and previous value
    of 'CF' is moved into 'f'
    ```
    f e d c b a 9 8 7 6 5 4 3 2 1 0   +   CF
    
    1 1 0 1 0 1 1 1 0 1 0 1 0 1 0 1   +   0
    ```
    ## EX.
    - RCR AL, CL (AL = 00011111 , CL = 3):
        1. 10001111 CL = 1  OF = 1
        2. 11000111 CL = 1  OF = 0
        3. 11100011 CL = 1  OF = 0
    - RCL AL, 1 (AL = 11111111):
        1. 01111111 CL = 1  OF = 1
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types']
    SOP = kwargs["source_params"]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"][0]
    INT = kwargs["args_values_int"][1]

    if PT[1] == "register" and SOP[1].upper() != "CL":
        return {"error" : {
            "popup" : "incorrect_param_bit_movement",
            "line" : kwargs["line"] + 1,
            "source_error" : None
        }}

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
    m = save_value_in_destination(HR, DS, value_to_shift, PT[0], DST)

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

#
#   Assign params range and allowed params combination for functions
#

for fn in [SAL, SAR, SHL, SHR, ROL, ROR, RCL, RCR]:
    fn.params_range = [2]
    fn.allowed_params_combinations = [
        ("memory", "value"), ("memory", "register"), ("register", "value"), 
        ("register", "register") ]
