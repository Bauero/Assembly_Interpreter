"""
This file is just small utility to quickly convet number representing values in flag reg.
to output, clearly telling user which flag are active - program expects to receive number
in one of the allowed forms:

0x10 | 10b | 0x10 | 10h | 1010 (treated as bin) | 12 (treated as dec) | ab (treated as hex.)

"""

from os import name, system
def clean_console(): system('cls' if name == 'nt' else 'clear')
def c_red(text):    return '\033[91m' + text + '\033[0m'
def c_green(text):  return '\033[92m' + text + '\033[0m'

def show_floags_to_value(value : str):
    """Print in console which flags are activated, given number as a string"""

    value = value.lower()

    #   Basic cases
    if    value.startswith("0b"):   value = value[2:]
    elif  value.endswith('b'):      value = value[:-1]
    elif  value.startswith('0x'):   value = bin(int(value, base=16))[2:]
    elif  value.endswith("h"):      value = bin(int(value[:-1], base=16))[2:]
    
    #   More advanced cases
    elif  only_binary(value):       value = value
    elif  only_decimal(value):      value = bin(int(value))[2:]
    elif  only_hexadecimal(value):  value = bin(int(value, base=16))[2:]
    else:
        print("Value is not recognized as number - showing flags impossible")
        return
    
    #   Adjust to always have 16 elements
    value = value.zfill(16)
    print()
    print(f"OF\t{c_green('True') if value[-12] == '1' else c_red('False')}\tOverflow Flag")
    print(f"DF\t{c_green('True') if value[-11] == '1' else c_red('False')}\tDirection Flag")
    print(f"IF\t{c_green('True') if value[-10] == '1' else c_red('False')}\tInterrupiton Flag")
    print(f"TF\t{c_green('True') if value[-9] == '1' else c_red('False')}\tTrap Flag")
    print(f"SF\t{c_green('True') if value[-8] == '1' else c_red('False')}\tSign Flag")
    print(f"ZF\t{c_green('True') if value[-7] == '1' else c_red('False')}\tZero Flag")
    print(f"AF\t{c_green('True') if value[-5] == '1' else c_red('False')}\tAxiliary Carry Flag")
    print(f"PF\t{c_green('True') if value[-3] == '1' else c_red('False')}\tParity Flag")
    print(f"CF\t{c_green('True') if value[-1] == '1' else c_red('False')}\tCarry Flag")

    

def only_binary(value):
    """Return True if number contains only 0 or 1"""
    for e in value:
        if e not in ["0", "1"]:
            return False
    return True

def only_decimal(value):
    """Return True if number contains only digits 0 to 9"""
    allowed_value = [str(f"{liczba}") for liczba in range(10)]
    for e in value:
        if e not in allowed_value:
            return False
    return True

def only_hexadecimal(value):
    """Return True if number contains only digits 0 to 9 or letters a to f"""
    allowed_value = [str(hex(liczba)[2:]).lower() for liczba in range(16)]
    for e in value:
        if e not in allowed_value:
            return False
    return True

if __name__ == "__main__":
    clean_console()
    x = input("Input number to display flags: ").strip()
    
    if not x:
        print("No input provided. Exiting ...") ; exit()
    
    show_floags_to_value(x)
