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
    """
    # ADJUST AFTER ADDITION.
    ## Description
    This function is designed to ajdust score after addition on number stored in BCD code.
    The purpose of this operation is to separate number stored in AL in binary form to 
    number stored in AH and AL in BCD form. What it does, is check if number in AL is greater
    than 9, or overflow to upper nible of AL occured (AF == 1), and if so, it adds one to 
    to AH, adds 6 to AL, sets both AF to 1 and CF to 1, and clears bits of upper nibble in 
    AL. This operation doesn't affect other flags.
    
    ## Summary:
    If (AL ^ 0Fh) > 9 or AF == 1 do the following:
    1. AL = AL + 6
    2. AH = AH + 1
    3. AF = 1
    4. CF = 1
    5. AL = AL ^ 0Fh

    ## EX:
    - AL = 00010110, AF = 1 -> AH += 1 -> AL += 6 (00011100) -> CF = 1, AF = 1 -> AL = AL ^ 15 -> AL = 12 (00001100)
    - AL = 10101010, AF = ? -> AH += 1 -> AL += 6 (10110000) -> CF = 1, AF = 1 -> AL = AL ^ 15 -> AL = 0  (00000000)
    - AL = 00001000, AF = 0 -> Nothing (conditions aren't met)
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
    """
    # ADJUST AFTER SUBSTRACTION.
    ## Description
    This function is designed to ajdust score after substraction on number stored in BCD code.
    
    The purpose of this operation is to separate number stored in AL in binary form to 
    number stored in AH and AL in BCD form. What it does, is check if number in AL is greater
    than 9, or overflow to upper nible of AL occured (AF == 1), and if so, it subtracts one to 
    from AH, subtracts 6 from AL, sets both AF to 1 and CF to 1, and clears bits of upper nibble in 
    AL. This operation doesn't affect other flags.
    
    ## Summary:
    If (AL ^ 0Fh) > 9 or AF == 1 do the following:
    1. AL = AL - 6
    2. AH = AH - 1
    3. AF = 1
    4. CF = 1
    5. AL = AL ^ 0Fh

    ## EX:
    - AL = 01001010, AF = 1 -> AH -= 1 -> AL -= 6 (01000100) -> CF = 1, AF = 1 -> AL = AL ^ 15 -> AL = 4  (00000100)
    - AL = 10101010, AF = ? -> AH -= 1 -> AL -= 6 (10100100) -> CF = 1, AF = 1 -> AL = AL ^ 15 -> AL = 4  (00000100)
    - AL = 00001000, AF = 0 -> Nothing (conditions aren't met)
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
    """
    # DECIMAL ADJUST FOR SUBSTRACTION
    ## Description
    Decimal adjustr after binary substraction in BCD code. This function performs the following
    operation. If lower nibble in AL is greater than 9 or AF is set, function substracts 6 from
    AL, and sets AF to 1. Then funciton check if AL is greater than 9Fh (159) or if the CF is set.
    If any of those conditions is met, funciton substracts 60h (96) from AL and sets CF to 1.
    This function influences flags SF, ZF, AF, PF, CF.
    
    ## Summary:
    0. if (AL ^ 0Fh) > 9 or AF == 1 do the following:
        1. AL = AL - 6;
        2. AF = 1
        3. if AL > 9Fh or CF = 1
            4. AL = AL - 60h
            5. CF = 1

    ## EX:
    - AL = 00000011, AF = 1 -> AL -= 6 (11111101) -> AF = 1 -> (AL > 9Fh) -> AL -= 96 (10100111) -> CF = 1
    - AL = 11101011, AF = 0 -> AL -= 6 (11100101) -> AF = 1 -> (AL > 9Fh) -> AL -= 96 (10000101) -> CF = 1
    - AL = 00001000, AF = 0 -> Nothing (conditions aren't met)
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
    """
    # DECIMAL ADJUST FOR ADDITION
    ## Description
    Decimal adjustr after binary addition in BCD code. This function performs the following
    operation. If lower nibble in AL is greater than 9 or AF is set, function adds 6 to
    AL, and sets AF to 1. Then funciton check if AL is greater than 9Fh (159) or if the CF is set.
    If any of those conditions is met, funciton adds 60h (96) to AL and sets CF to 1.
    This function influences flags SF, ZF, AF, PF, CF.
    
    ## Summary:
    0. if (AL ^ 0Fh) > 9 or AF == 1 do the following:
        1. AL = AL + 6;
        2. AF = 1
        3. if AL > 9Fh or CF = 1
            4. AL = AL + 60h
            5. CF = 1

    ## EX:
    - AL = 00000011, AF = 1 -> AL += 6 (00001001) -> AF = 1 -> (AL < 9Fh)
    - AL = 11101011, AF = 0 -> AL += 6 (11110001) -> AF = 1 -> (AL > 9Fh) -> AL += 96 (01010001) -> CF = 1
    - AL = 00001000, AF = 0 -> Nothing (conditions aren't met)
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
    """
    # ADJUST FOR MULTIPLY
    ## Description
    This function makes correction after multiplicaiton of two digits in BCD code.
    Internally this funciton divides AL by 10 and stores quotient in AH, while 
    reminder is stored in AL. Function sets flags SF, ZF, PF according to AX 
    value at the end of the operation.

    ## Summary:
    AH = AL // 10
    AL = AL mod 10
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
    ax_in_bits = ready_quotient + ready_reminder

    HR.writeIntoRegister("AH", converted_quotient)
    HR.writeIntoRegister("AL", converted_reminder)

    backup_flags = list(FR.readFlags())

    FR.setFlag("ZF", not "1" in ax_in_bits)
    FR.setFlag("SF", ax_in_bits[0] == "1")
    FR.setFlag("PF", eval_no_of_1(ax_in_bits))

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
    """
    # ADJUST FOR DIVISION
    ## Description
    This funciton allows to prepare BCD number for division. This operation adds value of
    AH, multiplied by 10 to AL, and then sets AH to 0 (equivalent to XOR AH, AH). Function 
    sets flags SF, ZF, PF according to AX value at the end of the operation.

    ## Summary:
    AL = AL + AH * 10
    AH = 0
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
    ax_as_str = "".join(new_al) + "".join(new_ah)

    HR.writeIntoRegister("AH", new_ah)
    HR.writeIntoRegister("AL", new_al)
    
    backup_flags = list(FR.readFlags())
    
    FR.setFlag("ZF", not "1" in ax_as_str)
    FR.setFlag("SF", ax_as_str[0] == "1")
    FR.setFlag("PF", eval_no_of_1(ax_as_str))

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
    """
    # ADD
    ## Description
    This function performs binary additon of two number, and then sets flags
    accoridingly. This influences flags OF, SF, ZF, AF, PF, CF.
    
    ## Summary
    Arg1 += Arg2

    ## EX.
    - ADD AX, 10 (for AX == 27) -> AX += 10 (00100101)
    """
    
    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
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
    m = save_value_in_destination(HR, DS, output, PT, DST)

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
    """
    # ADC
    ## Description
    This funciton works like ADD but after initial addition of two numbers, to 
    the destiation value of CF is added. This influences flags OF, SF, ZF, AF, PF, CF.
    
    ## Summary
    Arg1 += Arg2
    Arg1 += CF

    ## EX.
    - ADC AX, 10 (for AX == 27, CF = 1) -> AX += 11 (00100110)
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
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
    m = save_value_in_destination(HR, DS, output, PT, DST)

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
    """
    # SUB
    ## Description
    This function performs binary additon of two number as A - B is equivalent
    to A + B', where B' is two's compliment of B.
    This influences flags OF, SF, ZF, AF, PF, CF.
    
    ## Summary
    Arg1 -= Arg2

    ## EX.
    - SUB AX, 10 (for AX == 27) -> AX -= 10 (00010001)
    """
    
    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
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
    m = save_value_in_destination(HR, DS, output, PT, DST)
    
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
    """
    # SUB
    ## Description
    This funciton works like SUB, but it substracts value of CF form the result
    of A - B. Therefore it's equivalent to A - B - C, or A - (B + C). As in SUB
    function, we use the informaiton, that A-B is equal to A-B' if B' is two's
    compliment of B. Therefore SBB adds CF to B, calculates two's compliment of
    this value, and then performs addition of result to A.
    This influences flags OF, SF, ZF, AF, PF, CF.
    
    ## Summary
    Arg1 -= Arg2
    Arg1 -= CF

    ## EX.
    - SBB AX, 10 (for AX == 27, CF = 1) -> AX -= 11 (00010000)
    """
    
    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
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
    m = save_value_in_destination(HR, DS, output, PT, DST)

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
    """
    # COMPARE
    ## Description
    This function performs comparison between two operands to set flags
    accordingly. It is equivalend to SUB instruction, but in contrast to it, 
    CMP doesn't save output anywhere. Affects flags OF, SF, ZF, AF, PF, CF.
    
    ## Summary
    Calculate Arg1 - Arg2 -> set flags accoring to output
    """

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
    """
    # CONVERT BYTE WORD
    ## Descritpion
    Extends bit on position 7 in AL to AH, by taking it's value and filling each
    bit of AH with that value. Content of AL remains unchanged. Doesn't affect flags.
    
    ## EX:
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
    """
    # CONVERT WORD DOUBLEWORD
    ## Description
    Extends bit on position 15 in AX to DX, by taking it's value and filling each
    bit of DX with that value. Content of AX remains unchanged. Doesn't affect flags.
    
    ## EX:
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
    """
    # DECREMENT
    ## Description
    This instruction substract 1 from the argument, and store the new value inside
    source value. Affects flags OF, SF, ZF, AF, and PF accordingly.
    
    ## Summary
    Arg1 -= 1
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
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
    m = save_value_in_destination(HR, DS, output, PT, DST)

    all_changes = {
        m[0] : [ m[1] ],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def INC(**kwargs):
    """
    # INCREMENT
    ## Description
    This instruction adds 1 to the argument, and store the new value inside
    source value. Affects flags OF, SF, ZF, AF, and PF accordingly.
    
    ## Summary
    Arg1 += 1
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
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
    m = save_value_in_destination(HR, DS, output, PT, DST)

    all_changes = {
        m[0] : [ m[1] ],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def MUL(**kwargs):
    """
    # MULTIPLICATION
    ## Description
    This operation performs multiplication, which internally is equivalent to addition of
    multiple values of AX or AL, each left-shifted by the offset of another bit from the
    right. This function sets flags CF and OF if upper part of resutl - DX or AH depending
    on operaiton size - is not equal to 0; otherwise CF and OF is set to 0. Doesn't affect
    other flags.

    ## Summary
    ### Case 1 - multiply by 8 bit value
    `MUL byte 10` -> AX *= 10 -> if AH == 0 -> CF = 0 and OF = 0
    
    ### Case 2 - multiply by 16 bit value
    `MUL word 10` -> DX:AX *= 10 -> if DX == 0 -> CF = 0 and OF = 0
    """

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
    """
    # INTEGERS MULTIPLICATION
    ## Description
    This operation performs multiplication but takes into account sigh of the numbers.
    First, funciton finds two's compliment of argumenst (DX:AX or AX and funciton Argument)
    of those values which are negative. Then, it performs normal mutiplication. Then if sigs
    of numbers were not equal it calculates two's compliment of the result. Final value is
    stored in AX (for 8 bit multiplication) or DX:AX (for 16 bit multiplicaiton). Flags CF
    and OF are set if upper half doesn't only contains bits with value of the sign of lower
    half. (for 8 bit, if AH != 00000000 if AL 0??????? or AH != 11111111 if AL 1???????).
    Other flags are not changed.

    ## Summary
    ### Case 1 - multiply by 8 bit value
    `IMUL byte 10` -> AX *= 10; CBW AL != current AX value, set CF = 1 and OF = 1
    
    ### Case 2 - multiply by 16 bit value
    `IMUL word 10` -> DX:AX *= 10; CWD AX != current DX:AX value, set CF = 1 and OF = 1
    """

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
    """
    # DIVISION
    ## Description
    This funciton performs standard division treading both argumens as unsigned nubmers.
    First argument is always AX (for divisioin with byte-size value) or 
    DX:AX (for divisioin with word-size value). Quotient is stored in lover half, of first
    argument (AL or AX) and reminder in the upper half (AH or DX). This operation doesn't 
    affect any flags.

    ## Summary
    ### Case 1 - division with 8 bit number
    DIV byte 10 (for AX = 147) -> AH = 7 (00000111), AL = 14 (00001110)
    ### Case 2 - division with 16 bit number
    DIV word 10 (for DX:AX = 147) -> DX = 7 (0000000000000111), AX = 14 (0000000000001110)
    """

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
    """
    # INTIGER DIVISION
    ## Description
    This funciton performs division operation, while keeping sign of operation.
    First, funciton converts numbers to their's two's compliment equivalents if
    they are negative. Then typical division (as with DIV operation) is performed.
    At the end, if signs of numbers are not equal, two's compliment of the resutl
    is calculated, and stored inside AX or DX:AX. Other information are the same
    as in DIV instruciton. Funciton doesn't modify any flags.

    ## Summary
    ### Case 1 - division with 8 bit number
    DIV byte 10 (for AX = 147) -> AH = 7 (00000111), AL = 14 (00001110)
    ### Case 2 - division with 16 bit number
    DIV word 10 (for DX:AX = 147) -> DX = 7 (0000000000000111), AX = 14 (0000000000001110)
    """

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
    """
    # NEGATE
    ## Description
    This operation calculates two's compliment value of the arugment, and stores
    it in argument

    ## Summary
    Arg = 2's compliment value of the argument
    also equal to
    Arg = 0 - Arg + 1
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
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
    m = save_value_in_destination(HR, DS, output, PT, DST)

    all_changes = {
        m[0] : [m[1]],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

#
#   Assign params range and allowed params combination for funcitons
#

for fn in [ADD, ADC, SUB, SBB, CMP]:
    fn.params_range = [2]
    fn.allowed_params_combinations = [
    ("memory", "value"), ("memory", "register"), ("register", "register"), 
    ("register", "value"), ("register", "memory")
]

for fn in [INC, DEC, MUL, IMUL, DIV, IDIV, NEG]:
    fn.params_range = [1]
    fn.allowed_params_combinations = [ ("memory",), ("register",) ]

for fn in [AAA, AAS, DAA, DAS, AAM, AAD, CBW, CWD]:
    fn.params_range = [0]
    fn.allowed_params_combinations = [ tuple() ]
