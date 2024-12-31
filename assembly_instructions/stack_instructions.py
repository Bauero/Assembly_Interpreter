"""
This file contains instrucitons which are available to user to put or remove data from 
stack - all typical pop / push instructions which are avaialbe in assembly
"""

from hardware_registers import HardwareRegisters
from flag_register import FlagRegister
from stack import Stack
from datatypes import Data
from helper_functions import convert_number_to_int_with_binary_capacity, \
                             convert_number_to_bit_list, \
                             save_value_in_destination

list_of_registers = ['AX', 'CX', 'DX', 'BX', 'SP', 'BP', 'SI', 'DI']

################################################################################
#   FUNCTION DEFINITIONS
################################################################################

def PUSH(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function is responsible for writing value to stack. It works like this:
    
    1. Decrement SP by one - moves to next byte where content will be stored
    2. Write byte of data
    3. If there are more bytes, go back to step 1 ; otherwise stop"""

    SP = HardwareRegister.readFromRegister("SP")
    SP_value = convert_number_to_int_with_binary_capacity(SP, 16)
    SP_value_backup = SP_value
    
    value = kwargs['values'][0]
    final_size = kwargs['final_size']
    converted_value = convert_number_to_bit_list(value, final_size)
    no_bytes_conv_value = len(converted_value) // 8
    backup_stack = Stack.read(SP_value - no_bytes_conv_value, no_bytes_conv_value)

    Stack.write(SP_value, converted_value)
    SP_value -= no_bytes_conv_value

    output = {
        "stack" : [
            {
                "location" : SP_value_backup,
                "oryginal_value" :  list(map(int, backup_stack)),
                "new_value" :       list(map(int, converted_value))
            }
        ],
        "register" : [{
            "location" : "SP",
            "oryginal_value" :  list(map(int, bin(SP_value_backup)[2:])),
            "new_value" :       list(map(int, bin(SP_value)[2:]))
        }]
    }

    return output

def PUSHF(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function is responsible for writing flag register to stack. It works like this:
    
    1. Decrement SP by one - moves to next byte where content will be stored
    2. Write flag register into stack
    3. Decrement SP by one (2 bytes in total)"""

    SP = HardwareRegister.readFromRegister("SP")
    SP_value = convert_number_to_int_with_binary_capacity(SP, 16)
    SP_value_backup = SP_value
    SP_value -= 1
    
    value = list(FlagRegister.readFlags())
    backup_stack = Stack.read(SP_value - 2, 2)

    Stack.write(SP_value, value)
    SP_value -= 1

    output = {
        "stack" : [
            {
                "location" : SP_value_backup,
                "oryginal_value" :  list(map(int, backup_stack)),
                "new_value" :       list(map(int, value))
            }
        ],
        "register" : [{
            "location" : "SP",
            "oryginal_value" :  list(map(int, bin(SP_value_backup)[2:])),
            "new_value" :       list(map(int, bin(SP_value)[2:]))
        }]
    }

    return output

def PUSHA(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function is responsible for writing all registers to stack. It works like this:
    
    IMPORTANT:
    `The pushad instruction pushes EAX, ECX, EDX, EBX, ESP, EBP, ESI and EDI, in this order ...
    the push all and pop all instructions, including the pusha and popa instructions that push and pop the 16-bit registers.`
    - Introduction to 80x86 Assembly Language and Computer Architecture
    - Chapter: 5.4 for Loops in Assembly Language
    - ISBN 0-7637-1773-8

    -> This means, that register are pushed to the stack in the following order:

    AX, CX, DX, BX, SP, BP, SI, DI - SP, contains value it had before PUSHA instruction was executed

    1. Decrement SP by one - moves to next byte where content will be stored
    2. Write flag register into stack
    3. Decrement SP by one (2 bytes in total)"""

    reg_content = []

    for register in list_of_registers:
        reg_bits = HardwareRegister.readFromRegister(register)
        reg_value = convert_number_to_int_with_binary_capacity(reg_bits, 16)
        reg_content.append(reg_content)

    SP_value = reg_content[4]
    SP_backup = SP_value
    backup_stack = Stack.read(SP_value-17, 16)

    for value in reg_content:
        SP_value += 1
        Stack.write(SP_value, value)
        SP_value += 1

    values_on_stack = reg_content[-1:]

    output = {
        "stack" : [
            {
                "location" : SP_backup,
                "oryginal_value" :  list(map(int, backup_stack)),
                "new_value" :       list(map(int, values_on_stack))
            }
        ],
        "register" : [{
            "location" : "SP",
            "oryginal_value" :  list(map(int, bin(SP_backup)[2:])),
            "new_value" :       list(map(int, bin(SP_value)[2:]))
        }]
    }

    return output

def POP(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This functins pops value from stack. Inside it does the following:
    
    1. Read x bytes from the top of the stack (x, as it depends on the destinaiton)
    2. Store this value in the destination
    3. Incremenet value of the SP, by the amount of bytes red - this instruction
    doesn't "DELETE" the data - those bits are still phisically on the stack, but they
    are considered empty"""

    no_of_bytes = kwargs['final_size'] // 8

    SP = HardwareRegister.readFromRegister("SP")
    SP_value = convert_number_to_int_with_binary_capacity(SP, 16)
    SP_value_backup = SP_value

    values = Stack.read(SP_value, no_of_bytes)
    comb_value = list("".join(values))
    assert len(comb_value) // 8 == no_of_bytes
    
    m = save_value_in_destination(HardwareRegister, Data, Variables, comb_value, 
                              kwargs['param_types'][0], kwargs['source_params'][0])
    
    SP_value += no_of_bytes
    HardwareRegister.writeIntoRegister("SP", SP_value)

    if m[0] == "register":
        all_changes = {
            m[0] : [ m[1] , 
                {
                    "location" :        "SP",
                    "oryginal_value" :  list(map(int, bin(SP_value_backup)[2:])),
                    "new_value" :       list(map(int, bin(SP_value)[2:]))
                }      
            ]
        }

    else:
        all_changes = {
            m[0] : [ m[1] ],
            "register" : [
                {
                    "location" :        "SP",
                    "oryginal_value" :  list(map(int, bin(SP_value_backup)[2:])),
                    "new_value" :       list(map(int, bin(SP_value)[2:]))
                }
            ]
        }

    return all_changes

def POPF(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This functins pops last to bits from stack, and stores it in flag register"""

    SP = HardwareRegister.readFromRegister("SP")
    SP_value = convert_number_to_int_with_binary_capacity(SP, 16)
    SP_value_backup = SP_value

    values = Stack.read(SP_value, 2)
    comb_value = list("".join(values))
    
    flag_reg_backup = FlagRegister.readFlags()
    FlagRegister.setFlagRaw(comb_value)
    
    SP_value += 2
    HardwareRegister.writeIntoRegister("SP", SP_value)

    all_changes = {
       "register" : [ 
            {
                "location" :        "SP",
                "oryginal_value" :  list(map(int, bin(SP_value_backup)[2:])),
                "new_value" :       list(map(int, bin(SP_value)[2:]))
            }      
        ],
         "flags" : {
            "oryginal_value" :  list(flag_reg_backup),
            "new_value" :       list(comb_value)
        }
    }

    return all_changes

def POPA(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Stack : Stack,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This functins pops top 16 bits of data into the registers in this order:
    'DI', 'SI', 'BP', 'SP', 'BX', 'DX', 'CX', 'AX' """

    SP = HardwareRegister.readFromRegister("SP")
    SP_value = convert_number_to_int_with_binary_capacity(SP, 16)
    SP_value_backup = SP_value

    #   Save values of all registers, and then reverse the order of the list
    register_backups = [HardwareRegister.readFromRegister(r) for r in list_of_registers][-1:]

    #   Update all registers
    all_bytes = Stack.read(SP_value, 16)
    new_registers_values = []
    for i in range(0,16, 2):
        value = list("".join(all_bytes[i:i+2]))
        new_registers_values.append(value)
        register = list_of_registers[- (i // 2) - 1]
        HardwareRegister.writeIntoRegister(register, value)

    all_changes = {
        "register" : []
    }

    #   Generate history of changes for all registers
    for n, register in enumerate(list_of_registers[-1:]):
        all_changes["register"].append(
            {
                "location" :        register,
                "oryginal_value" :  list(map(int, register_backups[n])),
                "new_value" :       list(map(int, new_registers_values[n]))
            }
        )

    return all_changes

################################################################################
#   FUNCTION ATTRIBUTES
################################################################################

PUSH.params_range = [1]
PUSH.allowed_params_combinations = [ (1,), (2,), (3,), (4,), (5,), (6,), (7,) ]

PUSHF.params_range = [0]
PUSHF.allowed_params_combinations = [()]

PUSHA.params_range = [0]
PUSHA.allowed_params_combinations = [()]

POP.params_range = [1]
POP.allowed_params_combinations = [ (2,), (3,), (4,), (5,), (6,) ]

POPF.params_range = [0]
POPF.allowed_params_combinations = [()]

POPA.params_range = [0]
POPA.allowed_params_combinations = [()]
