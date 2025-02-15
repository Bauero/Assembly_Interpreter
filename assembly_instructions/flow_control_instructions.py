"""
This file contains instructions which modify flow of the program, but in contrast to jumps
they have it's own distinct function, and hence, deserve it's own file
"""

from datatypes import Data
from flag_register import FlagRegister
from hardware_registers import HardwareRegisters
from helper_functions import (save_value_in_destination,
                              convert_number_to_bit_list,
                              convert_number_to_bit_list,
                              convert_number_to_int_with_binary_capacity)

def LOOP(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function perfoms jump to the speciphied location if value in CX>0;
    
    1. Substract 1 from CX
    2. Compare if CX > 0
    3. If so, jump to label; if not, continue
    
    IMPORTANT:
    `... where statementLabel is the label of a statement that is a short displacement (128 bytes backward or 
    127 bytes forward) from the loop instruction.`
    - Introduction to 80x86 Assembly Language and Computer Architecture
    - Chapter: 5.4 for Loops in Assembly Language
    - ISBN 0-7637-1773-8

    IMPLEMENTATION:
    - Label points to instruction which is outside those boundaries, jump won't be
    executed, and value in CX won't change
    """

    CX = HardwareRegister.readFromRegister("CX")
    CX_value = convert_number_to_int_with_binary_capacity(CX, 16)

    current_line = kwargs['line']
    destination_line = kwargs['args_values_raw'][0]

    if current_line - destination_line <= 128 and current_line - destination_line >= -127:
        CX_value -= 1
        CX_binary = convert_number_to_bit_list(CX_value, 16)
        m = save_value_in_destination(HardwareRegister, Data, Variables,
                                      CX_binary, 3, "CX")
        
        if CX_value > 0:
            return { m[0] : [ m[1] ] }

def LOOPZ(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function perfoms jump to the speciphied location if value in CX>0 and ZF=1;
    
    1. Substract 1 from CX
    2. Compare if CX > 0 and ZF=1
    3. If so, jump to label; if not, continue
    
    IMPORTANT:
    `The loopz/loope instruction jumps if the new value in ECX is nonzero and the zero flag is set (ZF=1).`
    - Introduction to 80x86 Assembly Language and Computer Architecture
    - Chapter: 5.4 for Loops in Assembly Language
    - ISBN 0-7637-1773-8

    IMPLEMENTATION:
    - Label points to instruction which is outside those boundaries, jump won't be
    executed, and value in CX won't change
    """

    CX = HardwareRegister.readFromRegister("CX")
    CX_value = convert_number_to_int_with_binary_capacity(CX, 16)
    ZF = FlagRegister.readFlag("ZF")

    current_line = kwargs['line']
    destination_line = kwargs['args_values_raw'][0]

    if current_line - destination_line <= 128 and current_line - destination_line >= -127:
        CX_value -= 1
        CX_binary = convert_number_to_bit_list(CX_value, 16)
        m = save_value_in_destination(HardwareRegister, Data, Variables,
                                      CX_binary, 3, "CX")
        
        if CX_value > 0 and ZF:
            return { m[0] : [ m[1] ] }

def LOOPE(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function perfoms jump to the speciphied location if value in CX>0 and ZF=1;
    
    1. Substract 1 from CX
    2. Compare if CX > 0 and ZF=1
    3. If so, jump to label; if not, continue
    
    IMPORTANT:
    `The loopz/loope instruction jumps if the new value in ECX is nonzero and the zero flag is set (ZF=1).`
    - Introduction to 80x86 Assembly Language and Computer Architecture
    - Chapter: 5.4 for Loops in Assembly Language
    - ISBN 0-7637-1773-8

    IMPLEMENTATION:
    - Label points to instruction which is outside those boundaries, jump won't be
    executed, and value in CX won't change
    """

    CX = HardwareRegister.readFromRegister("CX")
    CX_value = convert_number_to_int_with_binary_capacity(CX, 16)
    ZF = FlagRegister.readFlag("ZF")

    current_line = kwargs['line']
    destination_line = kwargs['args_values_raw'][0]

    if current_line - destination_line <= 128 and current_line - destination_line >= -127:
        CX_value -= 1
        CX_binary = convert_number_to_bit_list(CX_value, 16)
        m = save_value_in_destination(HardwareRegister, Data, Variables,
                                      CX_binary, 3, "CX")
        
        if CX_value > 0 and ZF:
            return { m[0] : [ m[1] ] }

def LOOPNZ(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function perfoms jump to the speciphied location if value in CX>0 and ZF=0;
    
    1. Substract 1 from CX
    2. Compare if CX > 0 and ZF=0
    3. If so, jump to label; if not, continue
    
    IMPORTANT:
    `The loopnz/loopne instruction jumps if the new value in ECX is nonzero and the zero flag is clear (ZF=0).`
    - Introduction to 80x86 Assembly Language and Computer Architecture
    - Chapter: 5.4 for Loops in Assembly Language
    - ISBN 0-7637-1773-8

    IMPLEMENTATION:
    - Label points to instruction which is outside those boundaries, jump won't be
    executed, and value in CX won't change
    """

    CX = HardwareRegister.readFromRegister("CX")
    CX_value = convert_number_to_int_with_binary_capacity(CX, 16)
    ZF = FlagRegister.readFlag("ZF")

    current_line = kwargs['line']
    destination_line = kwargs['args_values_raw'][0]

    if current_line - destination_line <= 128 and current_line - destination_line >= -127:
        CX_value -= 1
        CX_binary = convert_number_to_bit_list(CX_value, 16)
        m = save_value_in_destination(HardwareRegister, Data, Variables,
                                      CX_binary, 3, "CX")
        
        if CX_value > 0 and not ZF:
            return { m[0] : [ m[1] ] }

def LOOPNE(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function perfoms jump to the speciphied location if value in CX>0 and ZF=0;
    
    1. Substract 1 from CX
    2. Compare if CX > 0 and ZF=0
    3. If so, jump to label; if not, continue
    
    IMPORTANT:
    `The loopnz/loopne instruction jumps if the new value in ECX is nonzero and the zero flag is clear (ZF=0).`
    - Introduction to 80x86 Assembly Language and Computer Architecture
    - Chapter: 5.4 for Loops in Assembly Language
    - ISBN 0-7637-1773-8

    IMPLEMENTATION:
    - Label points to instruction which is outside those boundaries, jump won't be
    executed, and value in CX won't change
    """

    CX = HardwareRegister.readFromRegister("CX")
    CX_value = convert_number_to_int_with_binary_capacity(CX, 16)
    ZF = FlagRegister.readFlag("ZF")

    current_line = kwargs['line']
    destination_line = kwargs['args_values_raw'][0]

    if current_line - destination_line <= 128 and current_line - destination_line >= -127:
        CX_value -= 1
        CX_binary = convert_number_to_bit_list(CX_value, 16)
        m = save_value_in_destination(HardwareRegister, Data, Variables,
                                      CX_binary, 3, "CX")
        
        if CX_value > 0 and not ZF:
            return { m[0] : [ m[1] ] }

def CALL(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    
    """This instructions perfoms call, which is quite similar to unconditional jump
    with push SP - instructions backups last line """

    label = kwargs['args_values_int'][0]
    label_in_bits = convert_number_to_bit_list(label, 16)

    SP = HardwareRegister.readFromRegister("SP")
    IP = HardwareRegister.readFromRegister("IP")
    SP_value = int(SP, base=2)
    SP_value_backup = SP_value
    SP_value -= 2
    
    backup_stack = Data.get_data(SP_value, 2)
    procc = map(lambda z: z.zfill(8), map(lambda x: x[2:], map(bin, backup_stack)))
    backup_stack = "".join(procc)

    Data.modify_data(SP_value, IP)
    HardwareRegister.writeIntoRegister("SP", SP_value)
    HardwareRegister.writeIntoRegister("IP", label)

    output = {
        "stack" : [
            {
                "location" : SP_value_backup,
                "oryginal_value" :  list(map(int, backup_stack)),
                "new_value" :       list(map(int, IP))
            }
        ],
        "register" : 
        [
            {
                "location" : "SP",
                "oryginal_value" :  list(map(int, bin(SP_value_backup)[2:])),
                "new_value" :       list(map(int, bin(SP_value)[2:]))
            },
            {
                "location" : "IP",
                "oryginal_value" :  list(map(int, IP)),
                "new_value" :       list(map(int, label_in_bits))
            }
        ],
        "next_instruction" : label
    }

    return output

def RET(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """Performs jump to address which is defined in 16 bit value to which SP points to.
    Equivalent to (although RET doesn't change any register except SP):
    ```
    POP AX
    JMP AX
    ```
    """

    no_of_bytes = 2
    SP = HardwareRegister.readFromRegister("SP")
    IP = HardwareRegister.readFromRegister("IP")
    SP_value = int(SP, base=2)
    SP_value_backup = SP_value

    values = Data.get_data(SP_value, no_of_bytes)
    procc = map(lambda z: z.zfill(8), map(lambda x: x[2:], map(bin, values)))
    list_values = "".join(procc)
    int_values = int(list_values, 2) + 1
    
    SP_value += no_of_bytes
    HardwareRegister.writeIntoRegister("SP", SP_value)
    HardwareRegister.writeIntoRegister("IP", int_values)

    all_changes = {
        "register" : [
            {
                "location" :        "SP",
                "oryginal_value" :  list(map(int, bin(SP_value_backup)[2:])),
                "new_value" :       list(map(int, bin(SP_value)[2:]))
            },
            {
                "location" :        "IP",
                "oryginal_value" :  list(map(int, IP)),
                "new_value" :       list(map(int, list_values))
            }
        ],
        "next_instruction" : int_values
    }
    
    return all_changes

for fn_name in list(filter(lambda n: n.upper() == n, dir())):
    """Assign all functions the same attributes"""
    fn = locals()[fn_name]
    if fn_name != "RET":
        fn.params_range = [1]
        fn.allowed_params_combinations = [("value",), ("label",)]
    else:
        fn.params_range = [0]
        fn.allowed_params_combinations = [tuple()]
