"""
This file contains operations which perform locical operations
"""

from program_code.helper_functions import (save_value_in_destination,
                                           convert_number_to_bit_list,
                                           eval_no_of_1,
                                           binary_or,
                                           binary_xor)

def AND(**kwargs):
    """
    # LOGICAL AND
    ## Description
    Performs logical AND operation on two numbers. For each bit of two numbers logical
    AND operation is performed, and result is stored in appropriate place in the result
    value. At the end, result value is stored in destination.
    Affectes flags OF, SF, ZF, PF, CF.
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    INT = kwargs["args_values_int"]

    and_value = INT[0] ^ INT[1]
    output = convert_number_to_bit_list(and_value, FS).zfill(FS)[-FS:]

    previous_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in output)
    FR.setFlag("SF", output[0] == "1")
    FR.setFlag("CF", 0)
    FR.setFlag("PF", eval_no_of_1(output))
    FR.setFlag("OF", 0)
    
    new_flags = list(FR.readFlags())
    m = save_value_in_destination(HR, DS, output, PT, DST)

    all_changes = {
        m[0] : [m[1]],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def OR(**kwargs):
    """
    # LOGICAL OR
    ## Description
    Performs logical OR operation on two numbers. For each bit of two numbers logical
    OR operation is performed, and result is stored in appropriate place in the result
    value. At the end, result value is stored in destination.
    Affectes flags OF, SF, ZF, PF, CF.
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]

    values_in_binary = [convert_number_to_bit_list(v, FS) for v in RAW]

    output, carry, auxiliary_carry = binary_or(FS, values_in_binary[0], 
                                                   values_in_binary[1])

    previous_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in output)
    FR.setFlag("SF", output[0] == "1")
    FR.setFlag("CF", 0)
    FR.setFlag("PF", eval_no_of_1(output))
    FR.setFlag("OF", 0)
    
    new_flags = list(FR.readFlags())
    m = save_value_in_destination(HR, DS, output, PT, DST)

    all_changes = {
        m[0] : [m[1]],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def XOR(**kwargs):
    """
    # LOGICAL XOR
    ## Description
    Performs logical XOR operation on two numbers. For each bit of two numbers logical
    XOR operation is performed, and result is stored in appropriate place in the result
    value. At the end, result value is stored in destination.
    Affectes flags OF, SF, ZF, PF, CF.
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]

    values_in_binary = [convert_number_to_bit_list(v, FS) for v in RAW]
        
    output, carry, auxiliary_carry = binary_xor(FS, values_in_binary[0], 
                                                    values_in_binary[1])

    previous_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in output)
    FR.setFlag("SF", output[0] == "1")
    FR.setFlag("CF", 0)
    FR.setFlag("PF", eval_no_of_1(output))
    FR.setFlag("OF", 0)
    
    new_flags = list(FR.readFlags())
    m = save_value_in_destination(HR, DS, output, PT, DST)

    all_changes = {
        m[0] : [m[1]],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def NOT(**kwargs):
    """
    # LOGICAL NOT
    ## Description
    Performs logical NOT operation on defined number. For each bit it stores it's opposite
    in appropriate place in the output number, and at the end stores final value in the
    desitinatin. Doesn't affect any flags.
    """

    HR  = kwargs["HR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]

    values_in_binary = [convert_number_to_bit_list(v, FS) for v in RAW]
    
    output = list(map(lambda x: str(int(not bool(int(x)))), values_in_binary[0]))[-FS:]

    m = save_value_in_destination(HR, DS, output, PT, DST)

    all_changes = {
        m[0] : [m[1]],
    }

    return all_changes

def NOP(**kwargs):
    """
    # NOTHING OPERATION
    ## Description
    This function does nothing - just takes time
    """

    return {}

def TEST(**kwargs):
    """
    # TEST
    ## Description
    This operation works exacly like AND operation, but doesn't store value anywhere. 
    This instruciton sets flags OF, SF, ZF, PF, CF.
    
    ## Summary
    Argumen1 ^ Argument2 -> Set flags accordingly
    """
    
    FR  = kwargs["FR"]
    FS  = kwargs['final_size']
    INT = kwargs["args_values_int"]

    and_value = INT[0] ^ INT[1]
    output = convert_number_to_bit_list(and_value, FS).zfill(FS)[-FS:]

    previous_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in output)
    FR.setFlag("SF", output[0] == "1")
    FR.setFlag("CF", 0)
    FR.setFlag("PF", eval_no_of_1(output))
    FR.setFlag("OF", 0)
    
    new_flags = list(FR.readFlags())
    
    all_changes = {
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

#
#   Assign params range and allowed params combination for functions
#

for fn in [AND, OR, XOR, TEST]:
    fn.params_range = [2]
    fn.allowed_params_combinations = [
        ("memory", "value"), ("memory", "register"), ("register", "register"), 
        ("register", "value"), ("register", "memory")
    ]

NOT.params_range = [1]
NOT.allowed_params_combinations = [ ("memory",), ("register",) ]

NOP.params_range = [0]
NOP.allowed_params_combinations = [tuple()]
