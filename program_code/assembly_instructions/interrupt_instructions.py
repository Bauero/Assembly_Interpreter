"""
This file contains all INT instructions which are possible to be Executed
"""

import time

def INT(**kwargs):
    """This function accepts"""

    HR = kwargs["HR"]
    AH = int(HR.readFromRegister("AH"), 2)

    hex_int_no = hex(kwargs["args_values_int"][0])[2:] + "h"
    interrupt = f"_int_{hex_int_no}_{AH}"

    specific_interrupt = all_instructions.get(interrupt, None)
    if not specific_interrupt:  return

    return specific_interrupt(**kwargs)

def _int_21h_2(**kwargs):
    
    HR = kwargs["HR"]
    DL = int(HR.readFromRegister("DL"), 2)

    return {"write_char_to_terminal" : DL}

def _int_21h_44(**kwargs):
    """This interrupt stores current time in CX and DX in the following format:
    
    - CH - Hours
    - CL - Minutes
    - DH - Seconds
    - DL - Miliseconds
    """

    HR = kwargs["HR"]
    CX = HR.readFromRegister("CX")
    DX = HR.readFromRegister("DX")

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

    HR.writeIntoRegister("CX", hours_minutes_combined)
    HR.writeIntoRegister("DX", sec_milisec_combined)

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

def _int_21h_0(**kwargs):
    
    return {"next_instruction" : -1}

def _int_21h_76(**kwargs):
    
    return {"next_instruction" : -1}

def _int_21h_10(**kwargs):

    return {"action_for_terminal" : "int_21h_10"}

INT.params_range = [1]
INT.allowed_params_combinations = [ ("value",) ]

all_instructions = locals()
