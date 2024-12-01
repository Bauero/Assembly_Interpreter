import re
from errors import WrongNumberBase, IncorectValueInListOfBits

def return_if_base_16_value(element : str) -> None | str:
    """Returns value if is a base 16 number, otherwise None"""
    if re.search(r"\b(0[xX][0-9a-fA-F]+|[0-9a-fA-F]+h)\b", element):
        if element.endswith('h'):
            element = "0x" + element[:-1] # "ADh" -> 0xAD
        return element
    
def return_if_base_10_value(element : str) -> None | str:    
    """Return value if is a base 10 number, otherwise None"""
    if re.search(r"\b(0|[1-9][0-9]*)\b", element):
        return element
    
def return_if_base_2_value(element : str) -> None | str:
    """Return value if is a base 2 number, otherwise None"""
    if re.search(r"\b[01]+[bB]\b", element):
        element = element[:-1]
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

def covert_number_to_bit_list(value : str | int | list, size : int = 8):
    
    assert type(size) == int, f"Size of number to convert cannot have different type than int" 
    assert size > 0, f"Cannot convert number to size which is less or equal to 0"
    assert size % 8 == 0, f"Cannot convert number, as the speciphied size is not mutiple of 8"
 
    def _convert_str(value):
        if  new_value := return_if_base_2_value(value):
            conv_value = list(new_value)
        elif new_value := return_if_base_16_value(value):
            conv_value = list(bin(int(new_value, base=16))[2:])
        elif return_if_base_10_value(value):
            conv_value = list(bin(int(value))[2:])
        else:
            raise WrongNumberBase(f"Number '{value}' seems to not belong to binary," +\
                                " decimal or hexadecimal numbers")
        return conv_value

    converted_value = []

    if type(value) == str:
        converted_value = _convert_str(value)
    elif type(value) == int:
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
    return converted_value[-size:]
    
def convert_number_to_bits_in_str(value : str | int | list, size = 8):
    """
    This function is 'wrapper' for `covert_number_to_bit_list`, and return value as a str
    and not a list
    """

    return "".join(covert_number_to_bit_list(value, size))

def convert_number_to_int_with_binary_capacity(value : str | int | list, size = 8):
    """
    This funciton returns int which is converted after directly translating either str, 
    int or list, to bits. This operation, although sligthly inefficent for int input
    or deicmal string, allows to confirm, that resulted value would fit in bit limit.
    """

    return int(convert_number_to_bits_in_str(value, size), base = 2)