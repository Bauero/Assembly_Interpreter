"""
This file contains all operations which perform arithmetic operations
"""

from hardware_registers import HardwareRegisters
from flag_register import FlagRegister
from datatypes import Data
from helper_functions import eval_no_of_1, sign_changed, convert_number_to_bit_list, \
                             inverse_Twos_Compliment_Number, save_value_in_destination, \
                             convert_number_to_bit_list,convert_number_to_int_with_binary_capacity

def AAA(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
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

    all_changes = None
    
    AL_source = HardwareRegister.readFromRegister("AL")
    AF = FlagRegister.readFlag("AF")
    al_int = int("".join(AL_source), 2)

    if (al_int ^ 15) > 9 or AF:
        al_int += 6
        al_int ^= 15
        AL_new = convert_number_to_bit_list(al_int, 8)
        HardwareRegister.writeIntoRegister(AL_new)
        
        AH_source = HardwareRegister.readFromRegister("AH")
        ah_int = int("".join(AH_source), 2)
        ah_int += 1
        AH_new = convert_number_to_bit_list(ah_int, 8)
        HardwareRegister.writeIntoRegister(AH_new)
        
        backup_flags = FlagRegister.readFlags()
        
        FlagRegister.setFlag("AF", 1)
        FlagRegister.setFlag("CF", 1)

        new_flags = FlagRegister.readFlags()

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

def AAS(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
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

    all_changes = None
    
    AL_source = HardwareRegister.readFromRegister("AL")
    AF = FlagRegister.readFlag("AF")
    al_int = int("".join(AL_source), 2)

    if (al_int ^ 15) > 9 or AF:
        al_int -= 6
        al_int ^= 15
        AL_new = convert_number_to_bit_list(al_int, 8)
        HardwareRegister.writeIntoRegister(AL_new)
        
        AH_source = HardwareRegister.readFromRegister("AH")
        ah_int = int("".join(AH_source), 2)
        ah_int -= 1
        AH_new = convert_number_to_bit_list(ah_int, 8)
        HardwareRegister.writeIntoRegister(AH_new)
        
        backup_flags = FlagRegister.readFlags()
        
        FlagRegister.setFlag("AF", 1)
        FlagRegister.setFlag("CF", 1)

        new_flags = FlagRegister.readFlags()

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

def DAS(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """DECIMAL ADJUST FOR SUBSTRACTION
    
    TLDR:
    if (AL ^ 0Fh) > 9 or AF == 1 do the following:
        1. AL = AL - 6;
        2. AF = 1
        
        if AL > 9Fh or CF = 1
            3.1. AL = AL - 60h
            3.2. CF = 1
    """

    all_changes = None
    
    AL_source = HardwareRegister.readFromRegister("AL")
    AF = FlagRegister.readFlag("AF")
    al_int = int("".join(AL_source), 2)

    if (al_int ^ 15) > 9 or AF:
        backup_flags = FlagRegister.readFlags()
        six_in_binary = convert_number_to_bit_list(6, 8)
        minus_six_in_binary = inverse_Twos_Compliment_Number(six_in_binary)

        output = []
        carry = 0
        auxiliary_carry = 0
        for bit in range(-1, - 8 -1, -1):
            b1 = int(AL_source[0][bit])
            b2 = int(minus_six_in_binary[1][bit])
            sum = b1 + b2 + carry
            carry = sum > 1
            output.insert(0, str(sum % 2))
            if abs(bit) == 4:
                auxiliary_carry = carry

        AL_after_add = output
        al_int = convert_number_to_int_with_binary_capacity(output, 8)
        FlagRegister.setFlag("AF", 1)

        if carry or al_int > 159:
            ninety_six_in_binary = convert_number_to_bit_list(96, 8)
            minus_ninety_six_in_binary = inverse_Twos_Compliment_Number(ninety_six_in_binary)

            output = []
            for bit in range(-1, - 8 -1, -1):
                b1 = int(AL_after_add[0][bit])
                b2 = int(minus_ninety_six_in_binary[1][bit])
                sum = b1 + b2 + carry
                carry = sum > 1
                output.insert(0, str(sum % 2))
                if abs(bit) == 4:
                    auxiliary_carry = carry

            FlagRegister.setFlag("CF", 1)

        FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
        FlagRegister.setFlag("SF", output[0] == "1")
        FlagRegister.setFlag("PF", eval_no_of_1(output))
        FlagRegister.setFlag("AF", auxiliary_carry)

        new_flags = FlagRegister.readFlags()

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

def DAA(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """DECIMAL ADJUST FOR ADDITION
    
    TLDR:
    if (AL ^ 0Fh) > 9 or AF == 1 do the following:
        1. AL = AL + 6;
        2. AF = 1
        
        if AL > 9Fh or CF = 1
            3.1. AL = AL + 60h
            3.2. CF = 1
    """

    all_changes = None
    
    AL_source = HardwareRegister.readFromRegister("AL")
    AF = FlagRegister.readFlag("AF")
    al_int = int("".join(AL_source), 2)

    if (al_int ^ 15) > 9 or AF:
        backup_flags = FlagRegister.readFlags()
        six_in_binary = convert_number_to_bit_list(6, 8)

        output = []
        carry = 0
        auxiliary_carry = 0
        for bit in range(-1, - 8 -1, -1):
            b1 = int(AL_source[0][bit])
            b2 = int(six_in_binary[1][bit])
            sum = b1 + b2 + carry
            carry = sum > 1
            output.insert(0, str(sum % 2))
            if abs(bit) == 4:
                auxiliary_carry = carry

        AL_after_add = output
        al_int = convert_number_to_int_with_binary_capacity(output, 8)
        FlagRegister.setFlag("AF", 1)

        if carry or al_int > 159:

            ninety_six_in_binary = convert_number_to_bit_list(96, 8)

            output = []
            for bit in range(-1, - 8 -1, -1):
                b1 = int(AL_after_add[0][bit])
                b2 = int(ninety_six_in_binary[1][bit])
                sum = b1 + b2 + carry
                carry = sum > 1
                output.insert(0, str(sum % 2))
                if abs(bit) == 4:
                    auxiliary_carry = carry

            FlagRegister.setFlag("CF", 1)

        FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
        FlagRegister.setFlag("SF", output[0] == "1")
        FlagRegister.setFlag("PF", eval_no_of_1(output))
        FlagRegister.setFlag("AF", auxiliary_carry)

        new_flags = FlagRegister.readFlags()

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

def AAM(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """ADJUST FOR MULTIPLY
    
    TLDR;
    AH = AL / 10
    AL = AL mod 10
    Sets flags SF, ZF, PF according to AL value at the beginning of the operation
    """

    AL = HardwareRegister.readFromRegister("AL")
    AH = HardwareRegister.readFromRegister("AH")

    divider = convert_number_to_int_with_binary_capacity(AL, 8)
    divisor = 10

    quotient = divider // divisor
    reminder = divider % divisor

    converted_quotient = convert_number_to_int_with_binary_capacity(quotient, 8)
    converted_reminder = convert_number_to_int_with_binary_capacity(reminder, 8)

    ready_quotient = bin(converted_quotient)[2:].zfill(8)
    ready_reminder = bin(converted_reminder)[2:].zfill(8)

    HardwareRegister.writeIntoRegister("AH", converted_quotient)
    HardwareRegister.writeIntoRegister("AL", converted_reminder)

    backup_flags = list(FlagRegister.readFlags())

    FlagRegister.setFlag("ZF", not "1" in AL)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", AL[0] == "1")
    FlagRegister.setFlag("PF", eval_no_of_1(AL))

    new_flags = list(FlagRegister.readFlags())

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

def AAD(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """ADJUST FOR DIVISION
    
    TLDR:
    AL = AL + AH * 10
    AH = 0
    Sets SF, ZF and PF accoring to final value in AL
    """

    AH = HardwareRegister.readFromRegister("AH")
    AL = HardwareRegister.readFromRegister("AL")

    ah_int = int("".join(AH),) * 10
    ah_bits = convert_number_to_bit_list(ah_int, 8)

    output = []
    carry = 0
    auxiliary_carry = 0
    for bit in range(-1, -9, -1):
        b1 = int(AL[0][bit])
        b2 = int(ah_bits[1][bit])
        sum = b1 + b2 + carry
        carry = sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry

    new_al = output
    new_ah = ['0' for _ in range(8)]

    HardwareRegister.writeIntoRegister("AH", new_ah)
    HardwareRegister.writeIntoRegister("AL", new_al)
    
    backup_flags = list(FlagRegister.readFlags())
    
    FlagRegister.setFlag("ZF", not "1" in new_al)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", new_al[0] == "1")
    FlagRegister.setFlag("PF", eval_no_of_1(new_al))

    new_flags = list(FlagRegister.readFlags())

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

def ADD(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function performs addition"""

    final_size = kwargs['final_size']

    # Convert both numbers to be in raw binary form -> 0111010110101101
    values_in_binary = []
    
    for v in kwargs['args_values_raw']:
        output = convert_number_to_bit_list(v, final_size)
        values_in_binary.append(output)
        
    # Perform binary addition
    output = []
    carry = 0
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        sum = b1 + b2 + carry
        carry = sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    previous_flags = list(FlagRegister.readFlags())

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", carry)
    FlagRegister.setFlag("PF", eval_no_of_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", sign_changed(values_in_binary[0],
                                            values_in_binary[1],
                                            output))

    new_flags = list(FlagRegister.readFlags())

    # Save value in the destination, and returned what have changed for history bilding
    m = save_value_in_destination(HardwareRegister, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])

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

def ADC(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This funciton performs ADD with carry"""

    final_size = kwargs['final_size']

    # Convert both numbers to be in raw binary form -> 0111010110101101
    values_in_binary = []
    
    for v in kwargs['args_values_raw']:
        output = convert_number_to_bit_list(v, final_size)
        values_in_binary.append(output)
        
    # Perform binary addition   
    output = []
    carry = FlagRegister.readFlag("CF")
    assert type(carry) == int, "Carry flag was red from the flag register, but it's type is not int"
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        sum = b1 + b2 + carry
        carry = sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    previous_flags = list(FlagRegister.readFlags())

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", carry)
    FlagRegister.setFlag("PF", eval_no_of_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", sign_changed(values_in_binary[0],
                                            values_in_binary[1],
                                            output))

    new_flags = list(FlagRegister.readFlags())

    # Save value in the destination
    m = save_value_in_destination(HardwareRegister, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])

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

def SUB(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function performs substraction (A - B)"""
    
    final_size = kwargs['final_size']
    values_in_binary = []
    
    for v in kwargs['args_values_raw']:
        output = convert_number_to_bit_list(v, final_size)
        values_in_binary.append(output)

    # Flip second number according to two's compliment rule (!x + 1 | 0011 -> 1101)
    values_in_binary[1] = inverse_Twos_Compliment_Number(values_in_binary[1])

    # Perform binary addition
    output = []
    carry = 0
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        sum = b1 + b2 + carry
        carry = sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    previous_flags = list(FlagRegister.readFlags())

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", carry)
    FlagRegister.setFlag("PF", eval_no_of_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", sign_changed(values_in_binary[0],
                                            values_in_binary[1],
                                            output))

    new_flags = list(FlagRegister.readFlags())

    # Save value in the destination, and returned what have changed for history bilding
    m = save_value_in_destination(HardwareRegister, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])
    
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

def SBB(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function performs substraction with borrow (A - B - CF)"""
    
    final_size = kwargs['final_size']
    values_in_binary = []
    
    for v in kwargs['args_values_raw']:
        output = convert_number_to_bit_list(v, final_size)
        values_in_binary.append(output)

    # Convert substracted value using the observation that: A - B - CF = A + ( -(B + CF) )
    assert type(values_in_binary[1]) == str
    CF = FlagRegister.readFlag("CF")
    assert type(CF) == int
    tmp = int(values_in_binary[1], base=2) + CF
    values_in_binary[1] = bin(tmp)[2:].zfill(32)[-32:]

    # Flip second number according to two's compliment rule (!x + 1 | 0011 -> 1101)
    values_in_binary[1] = inverse_Twos_Compliment_Number(values_in_binary[1])

    # Perform binary addition
    output = []
    carry = 0
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        sum = b1 + b2 + carry
        carry = sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    previous_flags = list(FlagRegister.readFlags())

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", carry)
    FlagRegister.setFlag("PF", eval_no_of_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", sign_changed(values_in_binary[0],
                                            values_in_binary[1],
                                            output))

    new_flags = list(FlagRegister.readFlags())

    # Save value in the destination, and returned what have changed for history bilding
    m = save_value_in_destination(HardwareRegister, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])

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

def CMP(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function performs comparison between two operands to set flags
    accordingly. It is equivalend to SUB instruction, but in contrast to it, 
    CMP doesn't save output anywhere"""

    final_size = kwargs['final_size']
    values_in_binary = []
    
    for v in kwargs['args_values_raw']:
        output = convert_number_to_bit_list(v, final_size)
        values_in_binary.append(output)

    # Flip second number according to two's compliment rule (!x + 1 | 0011 -> 1101)
    values_in_binary[1] = inverse_Twos_Compliment_Number(values_in_binary[1])

    # Perform binary addition
    output = []
    carry = 0
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        sum = b1 + b2 + carry
        carry = sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    previous_flags = list(FlagRegister.readFlags())

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", carry)
    FlagRegister.setFlag("PF", eval_no_of_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", sign_changed(values_in_binary[0],
                                            values_in_binary[1],
                                            output))

    new_flags = list(FlagRegister.readFlags())
    
    all_changes = {
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def DEC(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This instruction substract 1 from the argument, and store the new value inside
    source value. Affects flags OF, SF, ZF, AF, and PF accordingly"""

    final_size = kwargs['final_size']
    values_in_binary = []
    
    for v in kwargs['args_values_raw']:
        output = convert_number_to_bit_list(v, final_size)
        values_in_binary.append(output)

    #   Add binary numer, represeting 1 in binary, the size of final_size
    values_in_binary.append("0" * final_size-1 + "1")

    # Flip second number according to two's compliment rule (!x + 1 | 0011 -> 1101)
    values_in_binary[1] = inverse_Twos_Compliment_Number(values_in_binary[1])

    # Perform binary addition
    output = []
    carry = 0
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        sum = b1 + b2 + carry
        carry = sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    previous_flags = list(FlagRegister.readFlags())

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("PF", eval_no_of_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", sign_changed(values_in_binary[0],
                                            values_in_binary[1],
                                            output))

    new_flags = list(FlagRegister.readFlags())
    
    m = save_value_in_destination(HardwareRegister, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    all_changes = {
        m[0] : [ m[1] ],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def INC(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This instruction adds 1 to the argument, and store the new value inside
    source value. Affects flags OF, SF, ZF, AF, and PF accordingly"""

    final_size = kwargs['final_size']
    values_in_binary = []
    
    for v in kwargs['args_values_raw']:
        output = convert_number_to_bit_list(v, final_size)
        values_in_binary.append(output)

    #   Add binary numer, represeting 1 in binary, the size of final_size
    values_in_binary.append("0" * final_size-1 + "1")

    # Perform binary addition
    output = []
    carry = 0
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        sum = b1 + b2 + carry
        carry = sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    previous_flags = list(FlagRegister.readFlags())

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("PF", eval_no_of_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", sign_changed(values_in_binary[0],
                                            values_in_binary[1],
                                            output))

    new_flags = list(FlagRegister.readFlags())
    
    m = save_value_in_destination(HardwareRegister, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    all_changes = {
        m[0] : [ m[1] ],
        "flags" : {
            "oryginal_value" :  previous_flags,
            "new_value" :       new_flags
        }
    }

    return all_changes

def MUL(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function performs addition"""

    final_size = kwargs['final_size']

    # Convert both numbers to be in raw binary form -> 0111010110101101
    values_in_binary = []
    
    for v in kwargs['args_values_int']:
        output = convert_number_to_bit_list(v, final_size)
        values_in_binary.append(output)

    multiplied_numbers_for_addition = []

    for offset, bit in enumerate(range(-1, -final_size -1, -1)):
        multiplier = int(values_in_binary[1][bit])
        multiplied_bits = [str(int(b) & multiplier) for b in values_in_binary[0]]
        offseted_str = "".join(multiplied_bits) + "0" * offset
        ready_number = list(offseted_str.rjust(final_size*2, "0"))
        multiplied_numbers_for_addition.append(ready_number)

    all_auxiliary_carry = []
    carry = 0
    final_number = multiplied_numbers_for_addition.pop(0)
    for number in range(len(multiplied_numbers_for_addition)):
        output = []
        auxiliary_carry = 0
        for bit in range(-1, - (final_size*2) -1, -1):
            b1 = int(final_number[bit])
            b2 = int(multiplied_numbers_for_addition[number][bit])
            sum = b1 + b2 + carry
            carry = sum // 2
            output.insert(0, str(sum % 2))
            if abs(bit) == 4:
                auxiliary_carry = carry
        final_number = output
        all_auxiliary_carry.append(auxiliary_carry)

    # Resuce size of number if needed
    final_number = final_number[-final_size*2:]

    previous_flags = list(FlagRegister.readFlags())

    FlagRegister.setFlag("CF", "1" in final_number[:final_size])
    FlagRegister.setFlag("OF", "1" in final_number[:final_size])

    new_flags = list(FlagRegister.readFlags())

    upper_register = "AH" if final_size == 8 else "DX"
    lower_register = "AL" if final_size == 8 else "AX"
    oryginal_upper = HardwareRegister.readFromRegister(upper_register)
    oryginal_lower = HardwareRegister.readFromRegister(lower_register)
    new_upper = output[:final_size]
    HardwareRegister.readFromRegister(upper_register)
    new_lower = output[final_size:]
    HardwareRegister.readFromRegister(lower_register)

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

def IMUL(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function performs addition"""

    final_size = kwargs['final_size']

    # Convert both numbers to be in raw binary form -> 0111010110101101
    values_in_binary = []
    
    for v in kwargs['args_values_raw']:
        output = convert_number_to_bit_list(v, final_size)
        values_in_binary.append(output)

    n1_neg = values_in_binary[0][0] == "1"
    n2_neg = values_in_binary[1][0] == "1"

    if n1_neg:  values_in_binary[0] = list(inverse_Twos_Compliment_Number("".join(values_in_binary[0])))
    if n2_neg:  values_in_binary[1] = list(inverse_Twos_Compliment_Number("".join(values_in_binary[1])))

    multiplied_numbers_for_addition = []

    for offset, bit in enumerate(range(-1, -final_size -1, -1)):
        multiplier = int(values_in_binary[1][bit])
        multiplied_bits = [str(int(b) & multiplier) for b in values_in_binary[0]]
        offseted_str = "".join(multiplied_bits) + "0" * offset
        ready_number = list(offseted_str.rjust(final_size*2, "0"))
        multiplied_numbers_for_addition.append(ready_number)

    all_auxiliary_carry = []
    carry = 0
    final_number = multiplied_numbers_for_addition.pop(0)
    for number in range(len(multiplied_numbers_for_addition)):
        output = []
        auxiliary_carry = 0
        for bit in range(-1, - (final_size*2) -1, -1):
            b1 = int(final_number[bit])
            b2 = int(multiplied_numbers_for_addition[number][bit])
            sum = b1 + b2 + carry
            carry = sum // 2
            output.insert(0, str(sum % 2))
            if abs(bit) == 4:
                auxiliary_carry = carry
        final_number = output
        all_auxiliary_carry.append(auxiliary_carry)

    # Resuce size of number if needed
    final_number = final_number[-final_size*2:]   # {final_size} bits from the end

    if bool(n1_neg) ^ bool(n2_neg): 
        final_number = list(inverse_Twos_Compliment_Number("".join(final_number)))

    previous_flags = list(FlagRegister.readFlags())

    cf_of = [final_number[final_size] for _ in range(final_size)] != final_number[:final_size]

    FlagRegister.setFlag("CF", cf_of)
    FlagRegister.setFlag("OF", cf_of)

    new_flags = list(FlagRegister.readFlags())

    # Save value in the destination, and returned what have changed for history bilding
    upper_register = "AH" if final_size == 8 else "DX"
    lower_register = "AL" if final_size == 8 else "AX"
    oryginal_upper = HardwareRegister.readFromRegister(upper_register)
    oryginal_lower = HardwareRegister.readFromRegister(lower_register)
    new_upper = output[:final_size]
    HardwareRegister.readFromRegister(upper_register)
    new_lower = output[final_size:]
    HardwareRegister.readFromRegister(lower_register)

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

def DIV(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This operation performs division on unsigned numbers"""

    final_size = kwargs['final_size']
    divisor = kwargs['args_values_int'][0]

    upper = "AH" if final_size == 8 else "DX"
    lower = "AL" if final_size == 8 else "AX"

    upper_value = HardwareRegister.readFromRegister(upper)
    lower_value = HardwareRegister.readFromRegister(lower)

    divider = int(upper_value + lower_value, 2) 

    quotient = divider // divisor
    reminder = divider % divisor

    converted_quotient = convert_number_to_int_with_binary_capacity(quotient, final_size)
    converted_reminder = convert_number_to_int_with_binary_capacity(reminder, final_size)

    ready_quotient = bin(converted_quotient)[2:].zfill(final_size)
    ready_reminder = bin(converted_reminder)[2:].zfill(final_size)

    HardwareRegister.writeIntoRegister(upper, converted_reminder)
    HardwareRegister.writeIntoRegister(lower, converted_quotient)

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

def IDIV(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This operation performs division on signed numbers"""

    final_size = kwargs['final_size']
    divisor = kwargs['args_values_int'][0]

    upper = "AH" if final_size == 8 else "DX"
    lower = "AL" if final_size == 8 else "AX"

    upper_value = HardwareRegister.readFromRegister(upper)
    lower_value = HardwareRegister.readFromRegister(lower)

    n1_neg = upper_value[0] == "1"
    n2_neg = lower_value[0] == "1"

    if n1_neg:  upper_value = list(inverse_Twos_Compliment_Number("".join(upper_value)))
    if n2_neg:  lower_value = list(inverse_Twos_Compliment_Number("".join(lower_value)))

    divider = int(upper_value + lower_value, 2) 

    quotient = divider // divisor
    reminder = divider % divisor

    converted_quotient = convert_number_to_int_with_binary_capacity(quotient, final_size)
    converted_reminder = convert_number_to_int_with_binary_capacity(reminder, final_size)

    ready_quotient = bin(converted_quotient)[2:].zfill(final_size)
    ready_reminder = bin(converted_reminder)[2:].zfill(final_size)

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

    HardwareRegister.writeIntoRegister(upper, converted_reminder)
    HardwareRegister.writeIntoRegister(lower, converted_quotient)

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

def NEG(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This instruction saves up negated value of argument passed in destination"""

    final_size = kwargs['final_size']

    values_in_binary = [['1' for _ in range(final_size)]]

    output = convert_number_to_bit_list(kwargs['args_values_raw'][0], final_size)
    output = inverse_Twos_Compliment_Number(output)
    values_in_binary.append(output)

    output = []
    carry = 0
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        sum = b1 + b2 + carry
        carry = sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry
    
    values_in_binary = [output, convert_number_to_bit_list(1, final_size)]

    output = []
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        sum = b1 + b2 + carry
        carry = sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry

    m = save_value_in_destination(HardwareRegister, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])
    
    previous_flags = list(FlagRegister.readFlags())

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", 0)
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("PF", eval_no_of_1(output))
    FlagRegister.setFlag("OF", 0)

    new_flags = list(FlagRegister.readFlags())

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

for fn in [AAA, AAS, DAA, DAS, AAM, AAD]:
    """Assign all functions the same attributes"""
    fn.params_range = [0]
    fn.allowed_params_combinations = [ tuple() ]
