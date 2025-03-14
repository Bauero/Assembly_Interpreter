import re
import os
from .hardware_registers import HardwareRegisters
from .errors import (WrongNumberBase,
                    IncorectValueInListOfBits,
                    FileDoesntExist,
                    FileSizeMightBeTooBig,
                    FileTypeNotAllowed)

allowed_file_types = ['.asm']

def color_txt(text : str,
              color : str | None = None,
              font_size_px : int | None = None) -> str:
    fs = "font-size: {font_size_px}px;" if font_size_px else ""
    clr = "color: {color};" if color else ""
    return f'<pre><span style="{fs}{clr}">{text}</span></pre>'

def is_white_char(char):            return char in [' ', '\t']
def is_special(char):               return char in ['_', '@', '?']
def is_special_first(char):         return char in ['_', '@']
def is_rect_bracket(char):          return char in ['[', ']']
def is_arithmetic(char):            return char in ['+', '-', '/', '*']
def is_allowed_arithmetic(char):    return char in ['+', '*']
def is_valid_text(text):
    pattern = r"^(['\"])(?:\\.|(?!\1).)*\1$"
    output = re.match(pattern, text)
    return output != None

def is_allowed_var_name(char, count):
    if count == 0:
        return char.isalpha() or is_special_first(char)
    else:
        return char.isalnum() or is_special(char)

def return_if_base_16_value(element: str) -> None | str:
    """Returns value if it's a base 16 number, otherwise None"""
    
    if " " in element[-2:] or "\t" in element[-2:]: return
    element = element.replace(" ", "").replace("\t", "")
    if re.fullmatch(r"-?[ \t]*[0-9][0-9a-fA-F]*[hH]", element):
        return element[:-1]
    
def return_if_base_10_value(element: str) -> None | str:
    """Returns value if it's a base 10 number, otherwise None"""
    
    if " " in element[-2:] or "\t" in element[-2:]: return
    element = element.replace(" ", "").replace("\t", "")
    if re.fullmatch(r"(-[1-9][0-9]*|0|[1-9][0-9]*)[dD]?", element):
        return element[:-1] if element.lower().endswith("d") else element

def return_if_base_8_value(element: str) -> None | str:
    """Returns value if it's a base 8 number, otherwise None"""
    
    if " " in element[-2:] or "\t" in element[-2:]: return
    element = element.replace(" ", "").replace("\t", "")
    if re.fullmatch(r"(-[1-7][0-7]*|0|[1-7][0-7]*)[oOqQ]", element):
        return element[:-1]
    
def return_if_base_2_value(element: str) -> None | str:
    """Returns value if it's a base 2 number, otherwise None"""
    
    if " " in element[-2:] or "\t" in element[-2:]: return
    element = element.replace(" ", "").replace("\t", "")
    if re.fullmatch(r"(-?[ \t]?[1][01]*|0)[bB]", element):
        return element[:-1]

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

def return_name_from_size(size : int) -> str:

    match size:
        case 8:     return "byte"
        case 16:    return "word"
        case 32:    return "dword"
        case 64:    return "qword"
        case _:     return ""

def convert_number_to_bit_list(value : str | int | list, size : int = 8):
    """This function converts number to list of bits. It accepts either str, int or list
    as an input, and ensures that whatever the format is, the output will be in form of:
    
    -> `['1', '1',  '1', '0', '0', '1', '1', '0']` (for size == 8)
    """
    
    assert size > 0, f"Cannot convert number to size which is less or equal to 0"
    assert size % 8 == 0, f"Cannot convert number, as the specified size is not mutiple of 8"
 
    negative_value = False

    def _convert_str(value):
        if new_value := return_if_base_16_value(value):
            conv_value = bin(int(new_value, base=16))[2:]
        elif return_if_base_10_value(value):
            conv_value = bin(int(value))[2:]
        elif  new_value := return_if_base_2_value(value):
            conv_value = new_value[2:]
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
        converted_value = bin(value)[2:]
    elif type(value) == list:
        value = [str(e) for e in value] # ensure all elemetns in value are str
        for bit in value:
            if bit not in ['0', '1']:
                raise IncorectValueInListOfBits(f"Bit '{bit}' in list '{value}' is not '1' or '0'")
        converted_value = value
    
    #   Fill list with '0' if it's length is smaller than size
    adjusted_number = converted_value.zfill(size)[-size:]

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

def save_value_in_destination(HardwareRegister : HardwareRegisters, Data, value : list, 
                              destination_type : str, destination_value : str = ""):
    """This funciton saves value in destinaiton, and prepares response with change made"""

    oryginal_val : list | str = []

    match destination_type:
        case "register":
            oryginal_val = HardwareRegister.readFromRegister(destination_value)
            HardwareRegister.writeIntoRegister(destination_value, value)
        case "memory":
            size = len(value) // 8
            oryginal_val = Data.get_data(destination_value, size)
            Data.modify_data(destination_value, value)

    response = {
        "location" :        destination_value,
        "oryginal_value" :  list(oryginal_val),
        "new_value" :       list(value)
    }

    return destination_type, response

def eval_no_of_1(value : list | str):
    return not bool(list(value[-8:]).count("1") % 2)

def sign_changed(n1 : str, n2 : str, output : list):
    n1b, n2b = int(n1[0]), int(n2[0])
    if n1b == n2b and n1b != int(output[0]):
        return True
    return False

def binary_addition(bit_no : int, n1 : list, n2 : list, carry : int = 0, auxiliary_carry : int = 0):
    """This funciton performs binary addition of two numbers, and returns result with values of 
    carry flag and auxiliary carry flag after addition"""
    
    output = []
    
    for bit in range(-1, - bit_no - 1, -1):
        b1 = int(n1[bit])
        b2 = int(n2[bit])
        result = b1 + b2 + carry
        carry = result > 1
        output.insert(0, str(result % 2))
        if abs(bit) == 4:   auxiliary_carry = carry

    output = output[-bit_no:]

    return output, carry, auxiliary_carry

def binary_or(bit_no : int, n1 : list, n2 : list, carry : int = 0, auxiliary_carry : int = 0):
    """This funciton performs binary OR of two numbers, and returns result with values of 
    carry flag and auxiliary carry flag after addition"""
    
    output = []
    
    for bit in range(-1, - bit_no - 1, -1):
        b1 = int(n1[bit])
        b2 = int(n2[bit])
        result = str(int(b1 or b2))
        carry = result == 1
        output.insert(0, str(result))
        if abs(bit) == 4:   auxiliary_carry = carry

    output = output[-bit_no:]

    return output, carry, auxiliary_carry

def binary_xor(bit_no : int, n1 : list, n2 : list, carry : int = 0, auxiliary_carry : int = 0):
    """This funciton performs binary XOR of two numbers, and returns result with values of 
    carry flag and auxiliary carry flag after addition"""
    
    output = []
    
    for bit in range(-1, - bit_no - 1, -1):
        b1 = int(n1[bit])
        b2 = int(n2[bit])
        result = str(int((b1 or b2) and not (b1 and b2)))
        carry = b1 and b2
        output.insert(0, str(result))
        if abs(bit) == 4:   auxiliary_carry = carry

    output = output[-bit_no:]

    return output, carry, auxiliary_carry
