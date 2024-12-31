"""
This file contains all operations which perform arithmetic operations
"""

# from bit_operations import bitAddition
from hardware_registers import HardwareRegisters
from flag_register import FlagRegister
from stack import Stack
from datatypes import Data
from helper_functions import equal_no_of_0_1, sign_changed, convert_number_to_bit_list, \
                             inverse_Twos_Compliment_Number, save_value_in_destination

""" 
Allowed combinations, and it's numbers
    1. variable          (tmp1)
    2. [variable]        ([tmp1])
    3. register          (AX)
    4. [address_in_reg]  (word [BX])
    5. [address_value]   (word [20h])
    6. [combo_address]   ([BX+20h])
    7. value             (word 10h, or 20 or 10b)"""

################################################################################
#   FUNCTION DEFINITIONS
################################################################################

def ADD(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function performs addition"""

    final_size = kwargs['final_size']

    # Convert both numbers to be in raw binary form -> 0111010110101101
    values_in_binary = []
    
    for v in kwargs['values']:
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
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
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
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This funciton performs ADD with carry"""

    final_size = kwargs['final_size']

    # Convert both numbers to be in raw binary form -> 0111010110101101
    values_in_binary = []
    
    for v in kwargs['values']:
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
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
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
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function performs substraction (A - B)"""
    
    final_size = kwargs['final_size']
    values_in_binary = []
    
    for v in kwargs['values']:
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
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
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
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function performs substraction with borrow (A - B - CF)"""
    
    final_size = kwargs['final_size']
    values_in_binary = []
    
    for v in kwargs['values']:
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
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
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
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function performs comparison between two operands to set flags
    accordingly. It is equivalend to SUB instruction, but in contrast to it, 
    CMP doesn't save output anywhere"""

    final_size = kwargs['final_size']
    values_in_binary = []
    
    for v in kwargs['values']:
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
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
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
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This instruction substract 1 from the argument, and store the new value inside
    source value. Affects flags OF, SF, ZF, AF, and PF accordingly"""

    final_size = kwargs['final_size']
    values_in_binary = []
    
    for v in kwargs['values']:
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
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
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
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This instruction adds 1 to the argument, and store the new value inside
    source value. Affects flags OF, SF, ZF, AF, and PF accordingly"""

    final_size = kwargs['final_size']
    values_in_binary = []
    
    for v in kwargs['values']:
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
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
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

################################################################################
#   FUNCITON ATTRIBUTES
################################################################################

ADD.params_range = [2]
ADD.allowed_params_combinations = [
    (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
    (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
]

ADC.params_range = [2]
ADC.allowed_params_combinations = [
    (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
    (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
]

SUB.params_range = [2]
SUB.allowed_params_combinations = [
    (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
    (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
]

SBB.params_range = [2]
SBB.allowed_params_combinations = [
    (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
    (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
]

CMP.params_range = [2]
CMP.allowed_params_combinations = [
    (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
    (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
]

INC.params_range = [1]
INC.allowed_params_combinations = [ (2,), (3,) ]

DEC.params_range = [1]
DEC.allowed_params_combinations = [ (2,), (3,) ]
