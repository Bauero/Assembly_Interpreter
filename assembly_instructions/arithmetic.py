"""
This file contains all operations which perform arithmetic operations
"""

# from bit_operations import bitAddition
from hardware_registers import HardwareRegisters
from flag_register import FlagRegister
from stack import Stack
from datatypes import Data
from helper_functions import return_if_base_16_value, return_if_base_10_value, \
                                return_if_base_2_value, return_size_from_name, \
                                convert_number_to_int_with_binary_capacity,    \
                                inverse_Twos_Compliment_Number
from errors import WrongNumberBase

""" 
Allowed combinations, and it's numbers
    1. variable          (tmp1)
    2. [variable]        ([tmp1])
    3. register          (AX)
    4. [address_in_reg]  (word [BX])
    5. [address_value]   (word [20h])
    6. [combo_address]   ([BX+20h])
    7. value             (word 10h, or 20 or 10b)"""


def equal_no_of_0_1(value : list | str):
    count_0 = 0
    count_1 = 0
    for b in value:
        if b == "0":    count_0 += 1
        else:           count_1 += 1
    return count_0 == count_1

def sign_changed(n1 : str, n2 : str, output : list):
    n1b, n2b = int(n1[0]), int(n2[0])
    if n1b == n2b and n1b != int(output[0]):
        return True
    return False

def save_value_in_destination(HardwareRegister : HardwareRegisters,
                              Stack : Stack, Data : Data, Variables : dict,
                              value : list, destination : int, name : str = ""):

    oryginal_val = None
    modified = None

    match destination:
        case 2:
            name = name.split(" ")[-1][1:-1]
            start = Variables[name]['address']
            size = Variables[name]['size']
            oryginal_val = Data.get_data(start, size)
            modified = "variable"
            Data.modify_data(start, value)
        case 3:
            oryginal_val = HardwareRegister.readFromRegister(name)
            modified = "register"
            HardwareRegister.writeIntoRegister(name, value)
        case 4:
            size, address = name.split(" ")
            address = HardwareRegister.readFromRegister(name)
            address = convert_number_to_int_with_binary_capacity(address, 16)
            Data.modify_data(address, value)
        case 5:
            size, address = name.split(" ")
            size = return_size_from_name(size)
            address = convert_number_to_int_with_binary_capacity(address, 16)
            oryginal_val = Data.get_data(address, size)
            Data.modify_data(address, value)
        case 6:
            # TODO
            ...

    response = {
        "location" : name,
        "modified_type" : modified,
        "oryginal_value" : oryginal_val,
        "new_value" : value
    }

    return response



def ADD(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        **kwargs):
    """This function performs addition"""

    ADD.__setattr__('params_range', [2])
    ADD.__setattr__('allowed_params_combinations', [
        (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
        (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
    ])

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
        
    # Perform binary addition
    output = []
    carry = 0
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        sum = b1 + b2 + carry
        carry =  sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", carry)
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", sign_changed(values_in_binary[0],
                                            values_in_binary[1],
                                            output))

    # Save value in the destination, and returned what have changed for history bilding
    o = save_value_in_destination(HardwareRegister, Stack, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    return o

def ADC(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        **kwargs):
    """This funciton performs ADD with carry"""

    ADC.__setattr__('params_range', [2])
    ADC.__setattr__('allowed_params_combinations', [
        (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
        (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
    ])

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
        
    # Perform binary addition
    output = []
    carry = FlagRegister.readFlag("CF")
    assert type(carry) == int, "Carry flag was red from the flag register, but it's type is not int"
    auxiliary_carry = 0
    for bit in range(-1, - final_size -1, -1):
        b1 = int(values_in_binary[0][bit])
        b2 = int(values_in_binary[1][bit])
        sum = b1 + b2 + carry
        carry =  sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", carry)
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", sign_changed(values_in_binary[0],
                                            values_in_binary[1],
                                            output))

    # Save value in the destination
    o = save_value_in_destination(HardwareRegister, Stack, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    return o

def SUB(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        **kwargs):
    """This function performs substraction (A - B)"""
    
    SUB.__setattr__('params_range', [2])
    SUB.__setattr__('allowed_params_combinations', [
        (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
        (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
    ])
    
    final_size = kwargs['final_size']
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
        carry =  sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", carry)
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", sign_changed(values_in_binary[0],
                                            values_in_binary[1],
                                            output))

    # Save value in the destination, and returned what have changed for history bilding
    o = save_value_in_destination(HardwareRegister, Stack, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    return o

def SBB(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        **kwargs):
    """This function performs substraction with borrow (A - B - CF)"""
    
    SBB.__setattr__('params_range', [2])
    SBB.__setattr__('allowed_params_combinations', [
        (2, 3), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3),
        (4, 7), (5, 3), (5, 7), (6, 3), (6, 7)
    ])
    
    final_size = kwargs['final_size']
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

    # Convert substracted value using the observation that: A - B - CF = A + ( -(B + CF) )
    tmp = int(values_in_binary[1], base=2) + int(FlagRegister.readFlag("CF"))
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
        carry =  sum > 1
        output.insert(0, str(sum % 2))
        if abs(bit) == 4:
            auxiliary_carry = carry

    # Resuce size of number if needed
    output = output[-final_size:]   # {final_size} bits from the end

    # Set appriopriate flags
    FlagRegister.setFlag("ZF", not "1" in output)   # if any "1", ZF if OFF
    FlagRegister.setFlag("SF", output[0] == "1")
    FlagRegister.setFlag("CF", carry)
    FlagRegister.setFlag("PF", equal_no_of_0_1(output))
    FlagRegister.setFlag("AF", auxiliary_carry)
    FlagRegister.setFlag("OF", sign_changed(values_in_binary[0],
                                            values_in_binary[1],
                                            output))

    # Save value in the destination, and returned what have changed for history bilding
    o = save_value_in_destination(HardwareRegister, Stack, Data, Variables, output,
                             kwargs['param_types'][0], kwargs['source_params'][0])

    return o
