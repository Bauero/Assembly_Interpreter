"""
This file contains all operations which perform arithmetic operations
"""

from program_code.helper_functions import (eval_no_of_1,
                                           sign_changed,
                                           binary_addition,
                                           convert_number_to_bit_list, 
                                           inverse_Twos_Compliment_Number, 
                                           save_value_in_destination, 
                                           convert_number_to_bit_list, 
                                           convert_number_to_int_with_binary_capacity)


def AAA(**kwargs):
    """ADJUST AFTER ADDITION.
    This function is designed to ajdust score after addition on number stored in BCD code.
    
    TLDR:
    if (AL ^ 0Fh) > 9 or AF == 1 do the following:
        1. AL = AL + 6;
        2. AH = AH + 1;
        3. AF = 1
        4. CF = 1
        5. AL = AL ^ 0Fh
    """
    
    HR = kwargs["HR"]
    FR = kwargs["FR"]
    AF = FR.readFlag("AF")
    
    all_changes = None
    AL_source = HR.readFromRegister("AL")
    al_int = int("".join(AL_source), 2)

    if (al_int ^ 15) > 9 or AF:
        al_int += 6
        al_int ^= 15
        AL_new = convert_number_to_bit_list(al_int, 8)
        HR.writeIntoRegister(AL_new)
        
        AH_source = HR.readFromRegister("AH")
        ah_int = int("".join(AH_source), 2)
        ah_int += 1
        AH_new = convert_number_to_bit_list(ah_int, 8)
        HR.writeIntoRegister(AH_new)
        
        backup_flags = FR.readFlags()
        
        FR.setFlag("AF", 1)
        FR.setFlag("CF", 1)

        new_flags = FR.readFlags()

        all_changes = {
            "register" : [
                {
                    "location" :        "AL",
                    "oryginal_value" :  list(map(int, AL_source)),
                    "new_value" :       list(map(int, AL_new))
                },
                {
                    "location" :        "AH",
                    "oryginal_value" :  list(map(int, AH_source)),
                    "new_value" :       list(map(int, AH_new))
                }
            ],
            "flags" : {
                "oryginal_value" :  backup_flags,
                "new_value" :       new_flags
            }
        }

    return all_changes

def AAS(**kwargs):
    """ADJUST AFTER SUBSTRACTION.
    This function is designed to ajdust score after substraction on number stored in BCD code.
    
    TLDR:
    if (AL ^ 0Fh) > 9 or AF == 1 do the following:
        1. AL = AL - 6;
        2. AH = AH - 1;
        3. AF = 1
        4. CF = 1
        5. AL = AL ^ 0Fh
    """
    
    HR = kwargs["HR"]
    FR = kwargs["FR"]
    AF = FR.readFlag("AF")
    
    all_changes = None
    AL_source = HR.readFromRegister("AL")
    al_int = int("".join(AL_source), 2)

    if (al_int ^ 15) > 9 or AF:
        al_int -= 6
        al_int ^= 15
        AL_new = convert_number_to_bit_list(al_int, 8)
        HR.writeIntoRegister(AL_new)
        
        AH_source = HR.readFromRegister("AH")
        ah_int = int("".join(AH_source), 2)
        ah_int -= 1
        AH_new = convert_number_to_bit_list(ah_int, 8)
        HR.writeIntoRegister(AH_new)
        
        backup_flags = FR.readFlags()
        
        FR.setFlag("AF", 1)
        FR.setFlag("CF", 1)

        new_flags = FR.readFlags()

        all_changes = {
            "register" : [
                {
                    "location" :        "AL",
                    "oryginal_value" :  list(map(int, AL_source)),
                    "new_value" :       list(map(int, AL_new))
                },
                {
                    "location" :        "AH",
                    "oryginal_value" :  list(map(int, AH_source)),
                    "new_value" :       list(map(int, AH_new))
                }
            ],
            "flags" : {
                "oryginal_value" :  backup_flags,
                "new_value" :       new_flags
            }
        }

    return all_changes

def DAS(**kwargs):
    """DECIMAL ADJUST FOR SUBSTRACTION
    
    TLDR:
    if (AL ^ 0Fh) > 9 or AF == 1 do the following:
        1. AL = AL - 6;
        2. AF = 1
        
        if AL > 9Fh or CF = 1
            3.1. AL = AL - 60h
            3.2. CF = 1
    """
    
    HR = kwargs["HR"]
    FR = kwargs["FR"]
    AF = FR.readFlag("AF")

    all_changes = None
    AL_source = HR.readFromRegister("AL")
    al_int = int("".join(AL_source), 2)

    if (al_int ^ 15) > 9 or AF:
        backup_flags = FR.readFlags()
        six_in_binary = convert_number_to_bit_list(6, 8)
        minus_six_in_binary = inverse_Twos_Compliment_Number(six_in_binary)

        output, carry, auxiliary_carry = binary_addition(8, AL_source, 
                                                         minus_six_in_binary)

        AL_after_add = output
        al_int = convert_number_to_int_with_binary_capacity(output, 8)
        FR.setFlag("AF", 1)

        if carry or al_int > 159:
            ninety_six_in_binary = convert_number_to_bit_list(96, 8)
            minus_ninety_six_in_binary = inverse_Twos_Compliment_Number(ninety_six_in_binary)

            output, carry, auxiliary_carry = binary_addition(8, AL_after_add, 
                                                         minus_ninety_six_in_binary)

            FR.setFlag("CF", 1)

        FR.setFlag("ZF", not "1" in output)
        FR.setFlag("SF", output[0] == "1")
        FR.setFlag("PF", eval_no_of_1(output))
        FR.setFlag("AF", auxiliary_carry)

        new_flags = FR.readFlags()

        all_changes = {
            "register" : [
                {
                    "location" :        "AL",
                    "oryginal_value" :  list(map(int, AL_source)),
                    "new_value" :       list(map(int, output))
                }
            ],
            "flags" : {
                "oryginal_value" :  backup_flags,
                "new_value" :       new_flags
            }
        }

        return all_changes

def DAA(**kwargs):
    """DECIMAL ADJUST FOR ADDITION
    
    TLDR:
    if (AL ^ 0Fh) > 9 or AF == 1 do the following:
        1. AL = AL + 6;
        2. AF = 1
        
        if AL > 9Fh or CF = 1
            3.1. AL = AL + 60h
            3.2. CF = 1
    """
    
    HR = kwargs["HR"]
    FR = kwargs["FR"]
    AF = FR.readFlag("AF")
    
    all_changes = None
    AL_source = HR.readFromRegister("AL")
    al_int = int("".join(AL_source), 2)

    if (al_int ^ 15) > 9 or AF:
        backup_flags = FR.readFlags()
        six_in_binary = convert_number_to_bit_list(6, 8)

        output, carry, auxiliary_carry = binary_addition(8, AL_source, 
                                                         six_in_binary)

        AL_after_add = output
        al_int = convert_number_to_int_with_binary_capacity(output, 8)
        FR.setFlag("AF", 1)

        if carry or al_int > 159:
            ninety_six_in_binary = convert_number_to_bit_list(96, 8)

            output, carry, auxiliary_carry = binary_addition(8, AL_after_add, 
                                                         ninety_six_in_binary)

            FR.setFlag("CF", 1)

        FR.setFlag("ZF", not "1" in output)
        FR.setFlag("SF", output[0] == "1")
        FR.setFlag("PF", eval_no_of_1(output))
        FR.setFlag("AF", auxiliary_carry)

        new_flags = FR.readFlags()

        all_changes = {
            "register" : [
                {
                    "location" :        "AL",
                    "oryginal_value" :  list(map(int, AL_source)),
                    "new_value" :       list(map(int, output))
                }
            ],
            "flags" : {
                "oryginal_value" :  backup_flags,
                "new_value" :       new_flags
            }
        }

        return all_changes

def AAM(**kwargs):
    """ADJUST FOR MULTIPLY
    
    TLDR;
    AH = AL / 10
    AL = AL mod 10
    Sets flags SF, ZF, PF according to AL value at the beginning of the operation
    """
    
    HR = kwargs["HR"]
    FR = kwargs["FR"]
    AL = HR.readFromRegister("AL")
    AH = HR.readFromRegister("AH")

    divider = convert_number_to_int_with_binary_capacity(AL, 8)
    divisor = 10

    quotient = divider // divisor
    reminder = divider % divisor

    converted_quotient = convert_number_to_int_with_binary_capacity(quotient, 8)
    converted_reminder = convert_number_to_int_with_binary_capacity(reminder, 8)

    ready_quotient = bin(converted_quotient)[2:].zfill(8)
    ready_reminder = bin(converted_reminder)[2:].zfill(8)

    HR.writeIntoRegister("AH", converted_quotient)
    HR.writeIntoRegister("AL", converted_reminder)

    backup_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in AL)
    FR.setFlag("SF", AL[0] == "1")
    FR.setFlag("PF", eval_no_of_1(AL))

    new_flags = list(FR.readFlags())

    all_changes = {
        "register" : [
            {
                "location" :        "AH",
                "oryginal_value" :  list(map(int, AH)),
                "new_value" :       list(map(int, ready_quotient))
            },
            {
                "location" :        "AL",
                "oryginal_value" :  list(map(int, AL)),
                "new_value" :       list(map(int, ready_reminder))
            }
        ],
        "flags" : {
            "oryginal_value" :  backup_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def AAD(**kwargs):
    """ADJUST FOR DIVISION
    
    TLDR:
    AL = AL + AH * 10
    AH = 0
    Sets SF, ZF and PF accoring to final value in AL
    """
    
    HR = kwargs["HR"]
    FR = kwargs["FR"]
    AH = HR.readFromRegister("AH")
    AL = HR.readFromRegister("AL")

    ah_int = int("".join(AH),) * 10
    ah_bits = convert_number_to_bit_list(ah_int, 8)

    output, *_ = binary_addition(9, AL, ah_bits)

    new_al = output
    new_ah = ['0' for _ in range(8)]

    HR.writeIntoRegister("AH", new_ah)
    HR.writeIntoRegister("AL", new_al)
    
    backup_flags = list(FR.readFlags())
    
    FR.setFlag("ZF", not "1" in new_al)   # if any "1", ZF if OFF
    FR.setFlag("SF", new_al[0] == "1")
    FR.setFlag("PF", eval_no_of_1(new_al))

    new_flags = list(FR.readFlags())

    all_changes = {
        "register" : [
            {
                "location" :        "AH",
                "oryginal_value" :  list(map(int, AH)),
                "new_value" :       list(map(int, new_ah))
            },
            {
                "location" :        "AL",
                "oryginal_value" :  list(map(int, AL)),
                "new_value" :       list(map(int, new_al))
            }
        ],
        "flags" : {
            "oryginal_value" :  backup_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def ADD(**kwargs):
    """This function performs addition"""
    
    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]

    values_in_binary = [convert_number_to_bit_list(v, FS) for v in RAW]
        
    output, carry, auxiliary_carry = binary_addition(FS, values_in_binary[0], 
                                                         values_in_binary[1])

    previous_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in output)
    FR.setFlag("SF", output[0] == "1")
    FR.setFlag("CF", carry)
    FR.setFlag("PF", eval_no_of_1(output))
    FR.setFlag("AF", auxiliary_carry)
    FR.setFlag("OF", sign_changed(values_in_binary[0],
                                  values_in_binary[1],
                                  output))

    new_flags = list(FR.readFlags())
    m = save_value_in_destination(HR, DS, VAR, output, PT, DST)

    all_changes = {
        m[0] : [
            m[1]
        ],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def ADC(**kwargs):
    """This funciton performs ADD with carry"""

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]

    values_in_binary = [convert_number_to_bit_list(v, FS) for v in RAW]

    output, carry, auxiliary_carry = binary_addition(FS, values_in_binary[0], 
                                                         values_in_binary[1],
                                                         FR.readFlag("CF"))

    previous_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in output)
    FR.setFlag("SF", output[0] == "1")
    FR.setFlag("CF", carry)
    FR.setFlag("PF", eval_no_of_1(output))
    FR.setFlag("AF", auxiliary_carry)
    FR.setFlag("OF", sign_changed(values_in_binary[0],
                                  values_in_binary[1],
                                  output))

    new_flags = list(FR.readFlags())
    m = save_value_in_destination(HR, DS, VAR, output, PT, DST)

    all_changes = {
        m[0] : [
            m[1]
        ],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def SUB(**kwargs):
    """This function performs substraction (A - B)"""
    
    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]

    values_in_binary = [convert_number_to_bit_list(v, FS) for v in RAW]
    values_in_binary[1] = inverse_Twos_Compliment_Number(values_in_binary[1])

    output, carry, auxiliary_carry = binary_addition(FS, values_in_binary[0], 
                                                         values_in_binary[1])

    previous_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in output)
    FR.setFlag("SF", output[0] == "1")
    FR.setFlag("CF", carry)
    FR.setFlag("PF", eval_no_of_1(output))
    FR.setFlag("AF", auxiliary_carry)
    FR.setFlag("OF", sign_changed(values_in_binary[0],
                                  values_in_binary[1],
                                  output))

    new_flags = list(FR.readFlags())
    m = save_value_in_destination(HR, DS, VAR, output, PT, DST)
    
    all_changes = {
        m[0] : [
            m[1]
        ],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def SBB(**kwargs):
    """This function performs substraction with borrow (A - B - CF)"""
    
    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]
    CF = FR.readFlag("CF")
    
    values_in_binary = [convert_number_to_bit_list(v, FS) for v in RAW]

    # Convert substracted value using the observation that: A - B - CF = A + ( -(B + CF) )
    tmp = int("".join(values_in_binary[1]), base=2) + CF
    values_in_binary[1] = bin(tmp)[2:].zfill(32)[-32:]
    values_in_binary[1] = inverse_Twos_Compliment_Number(values_in_binary[1])
    
    output, carry, auxiliary_carry = binary_addition(FS, values_in_binary[0], 
                                                         values_in_binary[1])

    previous_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in output)
    FR.setFlag("SF", output[0] == "1")
    FR.setFlag("CF", carry)
    FR.setFlag("PF", eval_no_of_1(output))
    FR.setFlag("AF", auxiliary_carry)
    FR.setFlag("OF", sign_changed(values_in_binary[0],
                                  values_in_binary[1],
                                  output))

    new_flags = list(FR.readFlags())
    m = save_value_in_destination(HR, DS, VAR, output, PT, DST)

    all_changes = {
        m[0] : [
            m[1]
        ],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def CMP(**kwargs):
    """This function performs comparison between two operands to set flags
    accordingly. It is equivalend to SUB instruction, but in contrast to it, 
    CMP doesn't save output anywhere"""

    FR  = kwargs["FR"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]

    values_in_binary = [convert_number_to_bit_list(v, FS) for v in RAW]
    values_in_binary[1] = inverse_Twos_Compliment_Number(values_in_binary[1])

    output, carry, auxiliary_carry = binary_addition(FS, values_in_binary[0], 
                                                         values_in_binary[1])

    previous_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in output)
    FR.setFlag("SF", output[0] == "1")
    FR.setFlag("CF", carry)
    FR.setFlag("PF", eval_no_of_1(output))
    FR.setFlag("AF", auxiliary_carry)
    FR.setFlag("OF", sign_changed(values_in_binary[0],
                                  values_in_binary[1],
                                  output))

    new_flags = list(FR.readFlags())
    
    all_changes = {
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def CBW(**kwargs):
    """CONVERT BYTE WORD
    
    Extends bit on position 7 in AL to AH.
    
    EX:
    
    - AL = 01101010 -> AL [0] == 0 -> AX = 0000000001101010
    - AL = 10011101 -> AL [0] == 1 -> AX = 1111111110011101
    """

    HR  = kwargs["HR"]
    AL = HR.readFromRegister("AL")
    AH = HR.readFromRegister("AH")

    if AL[0] == "0":    new_ah = ["0" for _ in range(8)]
    else:               new_ah = ["1" for _ in range(8)]

    all_changes = {
        "register" : [
            {
                "location" :        "AH",
                "oryginal_value" :  list(map(int, AH)),
                "new_value" :       list(map(int, new_ah))
            },
        ]
    }

    return all_changes

def CWD(**kwargs):
    """CONVERT WORD DOUBLEWORD
    
    Extends bit on position 15 in AX to DX.
    
    EX:
    
    - AX = 0110101010110010 -> AX [0] == 0 -> DX:AX = 0000000000000000:0110101010110010
    - AX = 1001110110100111 -> AX [0] == 1 -> DX:AX = 1111111111111111:1001110110100111
    """
    HR = kwargs["HR"]
    AX = HR.readFromRegister("AX")
    DX = HR.readFromRegister("DX")

    if AX[0] == "0":    new_dx = ["0" for _ in range(16)]
    else:               new_dx = ["1" for _ in range(16)]

    all_changes = {
        "register" : [
            {
                "location" :        "DX",
                "oryginal_value" :  list(map(int, DX)),
                "new_value" :       list(map(int, new_dx))
            },
        ]
    }

    return all_changes

def DEC(**kwargs):
    """This instruction substract 1 from the argument, and store the new value inside
    source value. Affects flags OF, SF, ZF, AF, and PF accordingly"""

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]

    values_in_binary = [convert_number_to_bit_list(v, FS) for v in RAW]
    values_in_binary.append("0" * (FS-1) + "1")
    values_in_binary[1] = inverse_Twos_Compliment_Number(values_in_binary[1])

    output, carry, auxiliary_carry = binary_addition(FS, values_in_binary[0], 
                                                         values_in_binary[1])

    previous_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in output)
    FR.setFlag("SF", output[0] == "1")
    FR.setFlag("PF", eval_no_of_1(output))
    FR.setFlag("AF", auxiliary_carry)
    FR.setFlag("OF", sign_changed(values_in_binary[0],
                                  values_in_binary[1],
                                  output))

    new_flags = list(FR.readFlags())
    m = save_value_in_destination(HR, DS, VAR, output, PT, DST)

    all_changes = {
        m[0] : [ m[1] ],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def INC(**kwargs):
    """This instruction adds 1 to the argument, and store the new value inside
    source value. Affects flags OF, SF, ZF, AF, and PF accordingly"""

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]

    values_in_binary = [convert_number_to_bit_list(v, FS) for v in RAW]
    values_in_binary.append("0" * (FS-1) + "1")

    output, carry, auxiliary_carry = binary_addition(FS, values_in_binary[0], 
                                                         values_in_binary[1])

    previous_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in output)
    FR.setFlag("SF", output[0] == "1")
    FR.setFlag("PF", eval_no_of_1(output))
    FR.setFlag("AF", auxiliary_carry)
    FR.setFlag("OF", sign_changed(values_in_binary[0],
                                  values_in_binary[1],
                                  output))

    new_flags = list(FR.readFlags())
    m = save_value_in_destination(HR, DS, VAR, output, PT, DST)

    all_changes = {
        m[0] : [ m[1] ],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def MUL(**kwargs):
    """This function performs addition"""

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    FS  = kwargs['final_size']
    INT = kwargs["args_values_int"]

    values_in_binary = [convert_number_to_bit_list(v, FS) for v in INT]

    multiplied_numbers_for_addition = []

    for offset, bit in enumerate(range(-1, -FS -1, -1)):
        multiplier = int(values_in_binary[1][bit])
        multiplied_bits = [str(int(b) & multiplier) for b in values_in_binary[0]]
        offseted_str = "".join(multiplied_bits) + "0" * offset
        ready_number = list(offseted_str.rjust(FS*2, "0"))
        multiplied_numbers_for_addition.append(ready_number)

    all_auxiliary_carry = []
    carry = 0
    final_number = multiplied_numbers_for_addition.pop(0)
    for number in range(len(multiplied_numbers_for_addition)):
        output = []
        auxiliary_carry = 0
        for bit in range(-1, - (FS*2) -1, -1):
            b1 = int(final_number[bit])
            b2 = int(multiplied_numbers_for_addition[number][bit])
            sum = b1 + b2 + carry
            carry = sum // 2
            output.insert(0, str(sum % 2))
            if abs(bit) == 4:
                auxiliary_carry = carry
        final_number = output
        all_auxiliary_carry.append(auxiliary_carry)

    final_number = final_number[-FS*2:]

    previous_flags = list(FR.readFlags())

    FR.setFlag("CF", "1" in final_number[:FS])
    FR.setFlag("OF", "1" in final_number[:FS])

    new_flags = list(FR.readFlags())

    upper_register = "AH" if FS == 8 else "DX"
    lower_register = "AL" if FS == 8 else "AX"
    
    oryginal_upper = HR.readFromRegister(upper_register)
    oryginal_lower = HR.readFromRegister(lower_register)
    
    new_upper = output[:FS]
    new_lower = output[FS:]

    all_changes = {
        "register" : [
            {
                "location" :        upper_register,
                "oryginal_value" :  list(map(int, oryginal_upper)),
                "new_value" :       list(map(int, new_upper))
            },
            {
                "location" :        lower_register,
                "oryginal_value" :  list(map(int, oryginal_lower)),
                "new_value" :       list(map(int, new_lower))
            }
        ],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def IMUL(**kwargs):
    """This function performs addition"""

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]

    values_in_binary = [convert_number_to_bit_list(v, FS) for v in RAW]

    n1_neg = values_in_binary[0][0] == "1"
    n2_neg = values_in_binary[1][0] == "1"

    if n1_neg:
        values_in_binary[0] = list(inverse_Twos_Compliment_Number("".join(values_in_binary[0])))
    if n2_neg:
        values_in_binary[1] = list(inverse_Twos_Compliment_Number("".join(values_in_binary[1])))

    multiplied_numbers_for_addition = []

    for offset, bit in enumerate(range(-1, -FS -1, -1)):
        multiplier = int(values_in_binary[1][bit])
        multiplied_bits = [str(int(b) & multiplier) for b in values_in_binary[0]]
        offseted_str = "".join(multiplied_bits) + "0" * offset
        ready_number = list(offseted_str.rjust(FS*2, "0"))
        multiplied_numbers_for_addition.append(ready_number)

    all_auxiliary_carry = []
    carry = 0
    final_number = multiplied_numbers_for_addition.pop(0)
    for number in range(len(multiplied_numbers_for_addition)):
        output = []
        auxiliary_carry = 0
        for bit in range(-1, - (FS*2) -1, -1):
            b1 = int(final_number[bit])
            b2 = int(multiplied_numbers_for_addition[number][bit])
            sum = b1 + b2 + carry
            carry = sum // 2
            output.insert(0, str(sum % 2))
            if abs(bit) == 4:
                auxiliary_carry = carry
        final_number = output
        all_auxiliary_carry.append(auxiliary_carry)

    final_number = final_number[-FS*2:]

    if bool(n1_neg) ^ bool(n2_neg): 
        final_number = list(inverse_Twos_Compliment_Number("".join(final_number)))

    previous_flags = list(FR.readFlags())

    cf_of = [final_number[FS] for _ in range(FS)] != final_number[:FS]

    FR.setFlag("CF", cf_of)
    FR.setFlag("OF", cf_of)

    new_flags = list(FR.readFlags())
    
    upper_register = "AH" if FS == 8 else "DX"
    lower_register = "AL" if FS == 8 else "AX"
    
    oryginal_upper = HR.readFromRegister(upper_register)
    oryginal_lower = HR.readFromRegister(lower_register)
    
    new_upper = output[:FS]
    new_lower = output[FS:]

    all_changes = {
        "register" : [
            {
                "location" :        upper_register,
                "oryginal_value" :  list(map(int, oryginal_upper)),
                "new_value" :       list(map(int, new_upper))
            },
            {
                "location" :        lower_register,
                "oryginal_value" :  list(map(int, oryginal_lower)),
                "new_value" :       list(map(int, new_lower))
            }
        ],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def DIV(**kwargs):
    """This operation performs division on unsigned numbers"""

    HR  = kwargs["HR"]
    FS  = kwargs['final_size']
    
    divisor = kwargs['args_values_int'][0]

    upper = "AH" if FS == 8 else "DX"
    lower = "AL" if FS == 8 else "AX"

    upper_value = HR.readFromRegister(upper)
    lower_value = HR.readFromRegister(lower)

    divider = int(upper_value + lower_value, 2) 

    quotient = divider // divisor
    reminder = divider % divisor

    converted_quotient = convert_number_to_int_with_binary_capacity(quotient, FS)
    converted_reminder = convert_number_to_int_with_binary_capacity(reminder, FS)

    ready_quotient = bin(converted_quotient)[2:].zfill(FS)
    ready_reminder = bin(converted_reminder)[2:].zfill(FS)

    HR.writeIntoRegister(upper, converted_reminder)
    HR.writeIntoRegister(lower, converted_quotient)

    all_changes = {
        "register" : [
            {
                "location" :        upper,
                "oryginal_value" :  list(map(int, upper_value)),
                "new_value" :       list(map(int, ready_reminder))
            },
            {
                "location" :        lower,
                "oryginal_value" :  list(map(int, lower_value)),
                "new_value" :       list(map(int, ready_quotient))
            }
        ]
    }

    return all_changes

def IDIV(**kwargs):
    """This operation performs division on signed numbers"""

    HR = kwargs["HR"]
    FS  = kwargs['final_size']
    
    divisor = kwargs['args_values_int'][0]

    upper = "AH" if FS == 8 else "DX"
    lower = "AL" if FS == 8 else "AX"

    upper_value = HR.readFromRegister(upper)
    lower_value = HR.readFromRegister(lower)

    n1_neg = upper_value[0] == "1"
    n2_neg = lower_value[0] == "1"

    if n1_neg:  upper_value = list(inverse_Twos_Compliment_Number("".join(upper_value)))
    if n2_neg:  lower_value = list(inverse_Twos_Compliment_Number("".join(lower_value)))

    divider = int(upper_value + lower_value, 2) 

    quotient = divider // divisor
    reminder = divider % divisor

    converted_quotient = convert_number_to_int_with_binary_capacity(quotient, FS)
    converted_reminder = convert_number_to_int_with_binary_capacity(reminder, FS)

    ready_quotient = bin(converted_quotient)[2:].zfill(FS)
    ready_reminder = bin(converted_reminder)[2:].zfill(FS)

    if not n1_neg and not n2_neg:
        if ready_quotient[0] == "1":    Exception() # ready_quotient = inverse_Twos_Compliment_Number(ready_quotient)
        if ready_reminder[0] == "1":    Exception() # ready_reminder = inverse_Twos_Compliment_Number(ready_reminder)
    elif n1_neg and not n2_neg:
        if ready_quotient[0] == "0":    Exception() # ready_quotient = inverse_Twos_Compliment_Number(ready_quotient)
        if ready_reminder[0] == "0":    Exception() # ready_reminder = inverse_Twos_Compliment_Number(ready_reminder)
    elif not n1_neg and n2_neg:
        if ready_quotient[0] == "0":    Exception() # ready_quotient = inverse_Twos_Compliment_Number(ready_quotient)
        if ready_reminder[0] == "1":    Exception() # ready_reminder = inverse_Twos_Compliment_Number(ready_reminder)
    elif n1_neg and n2_neg:
        if ready_quotient[0] == "1":    Exception() # ready_quotient = inverse_Twos_Compliment_Number(ready_quotient)
        if ready_reminder[0] == "0":    Exception() # ready_reminder = inverse_Twos_Compliment_Number(ready_reminder)

    HR.writeIntoRegister(upper, converted_reminder)
    HR.writeIntoRegister(lower, converted_quotient)

    all_changes = {
        "register" : [
            {
                "location" :        upper,
                "oryginal_value" :  list(map(int, upper_value)),
                "new_value" :       list(map(int, ready_reminder))
            },
            {
                "location" :        lower,
                "oryginal_value" :  list(map(int, lower_value)),
                "new_value" :       list(map(int, ready_quotient))
            }
        ]
    }

    return all_changes

def NEG(**kwargs):
    """This instruction saves up negated value of argument passed in destination"""

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    VAR = kwargs["variables"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]

    values_in_binary = [list("1"*FS)]

    output = convert_number_to_bit_list(RAW[0], FS)
    output = inverse_Twos_Compliment_Number(output)
    values_in_binary.append(output)

    output, carry, auxiliary_carry = binary_addition(FS, values_in_binary[0], 
                                                         values_in_binary[1])
    
    values_in_binary = [output, convert_number_to_bit_list(1, FS)]

    output, carry, auxiliary_carry = binary_addition(FS, values_in_binary[0], 
                                                         values_in_binary[1],
                                                         carry)

    previous_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in output)
    FR.setFlag("SF", output[0] == "1")
    FR.setFlag("CF", 0)
    FR.setFlag("AF", auxiliary_carry)
    FR.setFlag("PF", eval_no_of_1(output))
    FR.setFlag("OF", 0)

    new_flags = list(FR.readFlags())
    m = save_value_in_destination(HR, DS, VAR, output, PT, DST)

    all_changes = {
        m[0] : [m[1]],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

for fn in [ADD, ADC, SUB, SBB, CMP]:
    """Assign all functions the same attributes"""
    fn.params_range = [2]
    fn.allowed_params_combinations = [
    ("memory", "value"), ("memory", "register"), ("register", "register"), 
    ("register", "value"), ("register", "memory")
]

for fn in [INC, DEC, MUL, IMUL, DIV, IDIV, NEG]:
    """Assign all functions the same attributes"""
    fn.params_range = [1]
    fn.allowed_params_combinations = [ ("memory",), ("register",) ]

for fn in [AAA, AAS, DAA, DAS, AAM, AAD, CBW, CWD]:
    """Assign all functions the same attributes"""
    fn.params_range = [0]
    fn.allowed_params_combinations = [ tuple() ]
