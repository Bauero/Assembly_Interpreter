"""
This file contains instrucitons which are available to user to put or remove data from 
stack - all typical pop / push instructions which are avaialbe in assembly
"""

from program_code.helper_functions import (convert_number_to_bit_list,
                                           save_value_in_destination)

list_of_registers = ['AX', 'CX', 'DX', 'BX', 'SP', 'BP', 'SI', 'DI']

def PUSH(**kwargs):
    """
    # PUSH VALUE TO STACK
    ## Description
    This function is responsible for writing value to stack. It works like this:
    
    1. Decrement SP by one - moves to next byte where content will be stored
    2. Write byte of data
    3. If there are more bytes, go back to step 1 ; otherwise stop
    
    ## IMPORTANT

    There is quite interesting behaviour implemented into NASM if we are operating
    on values smaller than 16 bits - basically, value provided is stretched to fit
    into 16 bits, and the stretching is done based on left-most bit:

    -> If we push 8 bit value left-most bit is coppied into all places:
    
    _ _ _ _ _ _ _ _     1 0 0 0 0 0 0 0
    
    1 1 1 1 1 1 1 1     1 0 0 0 0 0 0 0     -> 255  128

    ############################################################################

    _ _ _ _ _ _ _ _     0 1 1 1 0 1 0 1
    
    0 0 0 0 0 0 0 0     0 1 1 1 0 1 0 1     -> 000  117

    ## Raw example:

    Val                 First Byte  Second Byte

    - PUSH byte 127  -> 000         127
    - PUSH word 127  -> 000         127
    - PUSH byte 128  -> 255         128
    - PUSH word 128  -> 000         128
    - PUSH byte 260  -> 000         004
    - PUSH word 260  -> 001         004
    """

    HR  = kwargs["HR"]
    DS  = kwargs["DS"]
    FS  = kwargs['final_size']
    RAW = kwargs["args_values_raw"]
    SP  = HR.readFromRegister("SP")
    
    SP_value = int(SP, base=2)
    SP_value_backup = SP_value
    
    converted_value = convert_number_to_bit_list(RAW[0], FS)
    no_bytes_conv_value = len(converted_value) // 8
    
    SP_value -= no_bytes_conv_value
    backup_stack = DS.get_data(SP_value, no_bytes_conv_value)
    DS.modify_data(SP_value, converted_value)
    HR.writeIntoRegister("SP", SP_value)

    output = {
        "memory" : [
            {
                "location" :        SP_value,
                "oryginal_value" :  backup_stack,
                "new_value" :       converted_value
            }
        ],
        "register" : [{
            "location" : "SP",
            "oryginal_value" :  list(map(int, bin(SP_value_backup)[2:])),
            "new_value" :       list(map(int, bin(SP_value)[2:]))
        }]
    }

    return output

def PUSHF(**kwargs):
    """
    # PUSH VALUE OF FLAG REGISTER TO STACK
    ## Description
    This function is responsible for writing flag register to stack. It works like this:
    1. Decrement SP by one - moves to next byte where content will be stored
    2. Write flag register into stack
    3. Decrement SP by one (2 bytes in total)
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    SP = HR.readFromRegister("SP")
    
    SP_value = int(SP, base=2)
    SP_value_backup = SP_value
    SP_value -= 2
    
    value = list(FR.readFlags())
    backup_stack = DS.get_data(SP_value, 2)
    tmp = []
    for b in backup_stack:
        tmp.extend(list(bin(b)[2:]))

    procc = map(lambda z: z.zfill(8), map(lambda x: x[2:], map(bin, backup_stack)))
    backup_stack = "".join(procc)

    DS.modify_data(SP_value, value)
    HR.writeIntoRegister("SP", SP_value)

    output = {
        "memory" : [
            {
                "location" :        SP_value,
                "oryginal_value" :  backup_stack,
                "new_value" :       value
            }
        ],
        "register" : [{
            "location" : "SP",
            "oryginal_value" :  list(map(int, bin(SP_value_backup)[2:])),
            "new_value" :       list(map(int, bin(SP_value)[2:]))
        }]
    }
    return output

def PUSHA(**kwargs):
    """
    # PUSH VALUE OF ALL REGISTERS TO STACK
    ## Description
    This function is responsible for writing all registers to stack. It works like this:
    
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

    HR  = kwargs["HR"]
    DS  = kwargs["DS"]
    
    reg_content = []

    for register in list_of_registers:
        reg_bits = HR.readFromRegister(register)
        reg_content.append(reg_bits)

    SP = reg_content[4]
    SP_value = int(SP, 2)
    SP_backup = SP_value
    backup_stack = DS.get_data(SP_value-16, 16)
    procc = map(lambda z: z.zfill(8), map(lambda x: x[2:], map(bin, backup_stack)))
    backup_stack = "".join(procc)

    for value in reg_content:
        SP_value -= 2
        DS.modify_data(SP_value, value)

    HR.writeIntoRegister("SP", SP_value)
    values_on_stack = reg_content[-1::-1]
    bits_on_stack = "".join(values_on_stack)

    output = {
        "memory" : [
            {
                "location" :        SP_value,
                "oryginal_value" :  backup_stack,
                "new_value" :       bits_on_stack
            }
        ],
        "register" : [{
            "location" : "SP",
            "oryginal_value" :  list(map(int, bin(SP_backup)[2:])),
            "new_value" :       list(map(int, bin(SP_value)[2:]))
        }]
    }

    return output

def POP(**kwargs):
    """
    # POP VALUE FROM STACK
    ## Description
    This functins pops value from stack. Inside it does the following:
    
    1. Read x bytes from the top of the stack (x, as it depends on the destinaiton)
    2. Store this value in the destination
    3. Incremenet value of the SP, by the amount of bytes red - this instruction
    doesn't "DELETE" the data - those bits are still physically on the stack
    
    ## IMPORTANT

    Based on my experience with NASM, when we are POP'ing value from stack we need to store
    it in any place which would accept 16 bits - if we put in memory, in place where we
    store 8 bit variable, pop would return and store 16 bit, effectively overriting any
    byte which is stored in memory after the initial byte. Doing so in this simulator, if
    we push to 8 bit variable which is last in our data, would propably throw an error, as
    (in terms of memory) program reserves only the space which is declared by variables, while
    doing so in NASM for .COM program would *propably* just override any byte which is first
    in segment !
    """

    HR  = kwargs["HR"]
    DS  = kwargs["DS"]
    PT  = kwargs['param_types'][0]
    DST = kwargs["destination"]
    SP = HR.readFromRegister("SP")
    
    no_of_bytes = 2

    SP_value = int(SP, base=2)
    SP_value_backup = SP_value

    values = DS.get_data(SP_value, 2)
    procc = map(lambda z: z.zfill(8), map(lambda x: x[2:], map(bin, values)))
    comb_value = list("".join(procc))
    
    m = save_value_in_destination(HR, DS, comb_value, PT, DST)
    
    SP_value += no_of_bytes
    HR.writeIntoRegister("SP", SP_value)

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

def POPF(**kwargs):
    """
    # POP VALUE FROM STACK TO FLAG REGISTER
    ## Description
    This funciton reads first two bytes starting from the byte to which SP is currently
    pointing, and store those value in flag register. Flags are set accoring to values
    of corespoding bits.
    """

    HR  = kwargs["HR"]
    FR  = kwargs["FR"]
    DS  = kwargs["DS"]
    SP = HR.readFromRegister("SP")

    SP_value = int(SP, base=2)
    SP_value_backup = SP_value

    values = DS.get_data(SP_value, 2)
    procc = map(lambda z: z.zfill(8), map(lambda x: x[2:], map(bin, values)))
    comb_value = list("".join(procc))
    
    flag_reg_backup = FR.readFlags()
    FR.setFlagRaw(comb_value)
    
    SP_value += 2
    HR.writeIntoRegister("SP", SP_value)

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

def POPA(**kwargs):
    """
    # POP STACK VALUES INTO REGISTERS
    ## Description
    This functins pops top 16 bits of data into the registers in this order:
    1. DI
    2. SI
    3. BP
    4. SP
    5. BX
    6. DX
    7. CX
    8. AX
    """

    HR  = kwargs["HR"]
    DS  = kwargs["DS"]
    SP = HR.readFromRegister("SP")
    
    SP_value = int(SP, base=2)

    register_backups = [HR.readFromRegister(r) for r in list_of_registers][-1:]

    all_bytes = DS.get_data(SP_value, 16)
    new_registers_values = []
    for i in range(0,16, 2):
        procc = map(lambda z: z.zfill(8), map(lambda x: x[2:], map(bin, all_bytes[i:i+2])))
        value = list("".join(procc))
        new_registers_values.append(value)
        register = list_of_registers[- (i // 2) - 1]
        HR.writeIntoRegister(register, value)

    all_changes = {
        "register" : []
    }

    for n, register in enumerate(list_of_registers[-1:]):
        all_changes["register"].append(
            {
                "location" :        register,
                "oryginal_value" :  list(map(int, register_backups[n])),
                "new_value" :       list(map(int, new_registers_values[n]))
            }
        )

    return all_changes

#
#   Assign params range and allowed params combination for funcitons
#

PUSH.params_range = [1]
PUSH.allowed_params_combinations = [ ("memory",), ("register",), ("value",)]

POP.params_range = [1]
POP.allowed_params_combinations = [ ("memory",), ("register",) ]

for fn in [PUSHF, PUSHA, POPF, POPF]:
    fn.params_range = [0]
    fn.allowed_params_combinations = [ tuple() ]
