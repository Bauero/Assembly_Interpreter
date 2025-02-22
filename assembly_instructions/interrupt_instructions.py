"""
This file contains all INT instructions which are possible to be Executed
"""

import time
from hardware_registers import HardwareRegisters
from flag_register import FlagRegister
from datatypes import Data

def INT(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This function accepts"""

    AH = int(HardwareRegister.readFromRegister("AH"), 2)
    hex_int_no = hex(kwargs["args_values_int"][0])[2:] + "h"
    interrupt = f"_int_{hex_int_no}_{AH}"

    return globals()[interrupt](HardwareRegister,
                                FlagRegister,
                                Data,
                                Variables,
                                Labels,
                                **kwargs)

def _int_21h_2(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    
    DL = int(HardwareRegister.readFromRegister("DL"), 2)

    return {"write_char_to_terminal" : DL}

def _int_21h_44(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    """This interrupt stores current time in CX and DX in the following format:
    
    - CH - Hours
    - CL - Minutes
    - DH - Seconds
    - DL - Miliseconds
    """

    now = time.localtime()
    hours = now.tm_hour
    minutes = now.tm_min
    seconds = now.tm_sec
    mls = int((time.time() - int(time.time())) * 100)

    hours_bits = bin(hours)[2:].zfill(8)
    min_bits = bin(minutes)[2:].zfill(8)
    sec_bits = bin(seconds)[2:].zfill(8)
    msec_bits = bin(mls)[2:].zfill(8)

    hours_minutes_combined = list(hours_bits + min_bits)
    sec_milisec_combined = list(sec_bits + msec_bits)

    CX = HardwareRegister.readFromRegister("CX")
    DX = HardwareRegister.readFromRegister("DX")

    HardwareRegister.writeIntoRegister("CX", hours_minutes_combined)
    HardwareRegister.writeIntoRegister("DX", sec_milisec_combined)

    output = {
        "register" : [
            {
                "location" : "CX",
                "oryginal_value" :  CX,
                "new_value" :       hours_minutes_combined
            },
            {
                "location" : "DX",
                "oryginal_value" :  DX,
                "new_value" :       sec_milisec_combined
            }
        ]
    }

    return output

def _int_21h_0(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    
    return {"next_instruction" : -1}

def _int_21h_76(HardwareRegister : HardwareRegisters, 
        FlagRegister : FlagRegister,
        Data : Data,
        Variables : dict,
        Labels : dict,
        **kwargs):
    
    return {"next_instruction" : -1}

INT.params_range = [1]
INT.allowed_params_combinations = [ ("value",) ]
