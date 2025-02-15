import re
import os
from hardware_registers import HardwareRegisters
from errors import (WrongNumberBase,
                    IncorectValueInListOfBits,
                    FileDoesntExist,
                    FileSizeMightBeTooBig,
                    FileTypeNotAllowed)

allowed_file_types = ['.s','.asm']

def is_white_char(char):            return char in [' ', '\t']
def is_special(char):               return char in ['_', '@', '?']
def is_special_first(char):         return char in ['_', '@']
def is_rect_bracket(char):          return char in ['[', ']']
def is_arithmetic(char):            return char in ['+', '-', '/', '*']
def is_allowed_arithmetic(char):    return char in ['+', '*']

def is_allowed_var_name(char, count):
    if count == 0:
        return char.isalpha() or is_special_first(char)
    else:
        return char.isalnum() or is_special(char)

def return_if_base_16_value(element : str) -> None | str:
    """Returns value if is a base 16 number, otherwise None"""
    if re.search(r"\b(0[xX][0-9a-fA-F]+|[0-9a-fA-F]+h)\b", element):
        if element.endswith('h'):
            negative = element.startswith("-")
            if negative:    element = element[1:]
            sign = "-" if negative else ""
            element = sign + "0x" + element[:-1]
        return element
    
def return_if_base_10_value(element : str) -> None | str:    
    """Return value if is a base 10 number, otherwise None"""
    if re.search(r"\b(0|[1-9][0-9]*)\b", element):
        return element

def return_if_base_8_value(element : str) -> None | str:    
    """Return value if is a base 8 number, otherwise None"""
    if re.search(r"\b(0|[1-9][0-9]*)\b", element):
        return element
    
def return_if_base_2_value(element : str) -> None | str:
    """Return value if is a base 2 number, otherwise None"""
    if re.search(r"\b[01]+[bB]\b", element):
        element = '0b' + element[:-1]
        return element
    
def return_size_from_name(name : str):

    match name.lower():
        case "byte":    return 8
        case 'db':      return 8
        case "word":    return 16
        case 'dw':      return 16
        case "dword":   return 32
        case 'dd':      return 32
        case "qword":   return 64
        case 'dq':      return 64
        case _:         return -1

def convert_number_to_bit_list(value : str | int | list, size : int = 8):
    """This function converts number to list of bits. It accepts either str, int or list
    as an input, and ensures that whatever the format is, the output will be in form of:
    
    -> `['1', '1',  '1', '0', '0', '1', '1', '0']` (for size == 8)
    """
    
    assert type(size) == int, f"Size of number to convert cannot have different type than int" 
    assert size > 0, f"Cannot convert number to size which is less or equal to 0"
    assert size % 8 == 0, f"Cannot convert number, as the speciphied size is not mutiple of 8"
 
    negative_value = False

    def _convert_str(value):
        if new_value := return_if_base_16_value(value):
            conv_value = list(bin(int(new_value, base=16))[2:])
        elif return_if_base_10_value(value):
            conv_value = list(bin(int(value))[2:])
        elif  new_value := return_if_base_2_value(value):
            conv_value = list(new_value)
        else:
            raise WrongNumberBase(f"Number '{value}' seems to not belong to binary," +\
                                " decimal or hexadecimal numbers")
        return conv_value

    converted_value = []

    if type(value) == str:
        if value[0] == "-":
            negative_value = True
            value = value[1:].strip()
        converted_value = _convert_str(value)
    elif type(value) == int:
        if value < 0:   negative_value = True
        value = abs(value)
        converted_value = list(bin(value)[2:])
    elif type(value) == list:
        value = [str(e) for e in value] # ensure all elemetns in value are str
        for bit in value:
            if bit not in ['0', '1']:
                raise IncorectValueInListOfBits(f"Bit '{bit}' in list '{value}' is not '1' or '0'")
        converted_value = value
    
    #   Fill list with '0' if it's length is smaller than size
    while len(converted_value) < size:  converted_value.insert(0, '0')

    #   Get {size} bits from the end - cut any bits which woulnd't fit in specified size
    adjusted_number = converted_value[-size:]

    if negative_value:
        adjusted_number_str = "".join(adjusted_number)
        return list(inverse_Twos_Compliment_Number(adjusted_number_str))
    
    else:
        return adjusted_number
    
def convert_number_to_bits_in_str(value : str | int | list, size = 8):
    """
    This function is 'wrapper' for `convert_number_to_bit_list`, and return value as a str
    and not a list
    """

    return "".join(convert_number_to_bit_list(value, size))

def convert_number_to_int_with_binary_capacity(value : str | int | list, size = 8):
    """
    This funciton returns int which is converted after directly translating either str, 
    int or list, to bits. This operation, although sligthly inefficent for int input
    or deicmal string, allows to confirm, that resulted value would fit in bit limit.
    """

    return int(convert_number_to_bits_in_str(value, size), base = 2)

def loadFileFromPath(path_to_file : str, 
              ignore_size_limit : bool = False,
              ignore_file_type : bool = False) -> list | Exception:
    """
    This function loads file (if one exist) and returns loaded file as subscribtable
    object for further processing.

    :param:
    - `ignore_size_limit` : bool - allow to process file above 1MB
    - `ignore_file_type` : bool - allow to process file with extenstion other than .s or .asm
    """

    if not os.path.exists(path_to_file):
        raise FileDoesntExist(path_to_file)
    elif not ignore_size_limit and os.path.getsize(path_to_file) > 1000000: # > 1MB
        raise FileSizeMightBeTooBig(path_to_file)
    elif not ignore_file_type and \
        (ext := os.path.splitext(path_to_file)[-1]) not in allowed_file_types:
        raise FileTypeNotAllowed(ext)

    raw_file = []

    with open(path_to_file) as file:
        for line in file:
            raw_file.append(line)

    return raw_file

def inverse_Twos_Compliment_Number(value : str):

    """Convert value to two's compliment of the source value and return it"""

    if value[0] == "0":
        # Inverse value
        value = "".join(["1" if x == "0" else "0" for x in value])
        # + 1
        output = bin(int(value, base=2) + 1)[2:].zfill(len(value))[-len(value):]
    else:
        # - 1
        value = bin(int(value, base=2) - 1)[2:].zfill(len(value))[-len(value):]
        # Inverse value
        output = "".join(["1" if x == "0" else "0" for x in value])

    return output

def save_value_in_destination(HardwareRegister : HardwareRegisters, Data, Variables : dict,
                              value : list, destination : int, name : str = ""):

    oryginal_val : list | str = []
    modified = None

    match destination:
        case "register":
            oryginal_val = HardwareRegister.readFromRegister(name)
            modified = "register"
            HardwareRegister.writeIntoRegister(name, value)
        case "memory":
            name = name.split(" ")[-1][1:-1]
            start = Variables[name]['address']
            size = Variables[name]['size']
            oryginal_val = Data.get_data(start, size)
            modified = "variable"
            Data.modify_data(start, value)

    response = {
        "location" :        name,
        "oryginal_value" :  list(map(int, oryginal_val)),
        "new_value" :       list(map(int, value))
    }

    return modified, response

def eval_no_of_1(value : list | str):
    return not bool(list(value[-8:]).count("1") % 2)

def sign_changed(n1 : str, n2 : str, output : list):
    n1b, n2b = int(n1[0]), int(n2[0])
    if n1b == n2b and n1b != int(output[0]):
        return True
    return False
