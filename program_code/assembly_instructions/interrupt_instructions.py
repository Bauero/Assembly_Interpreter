"""
This file contains all INT instructions which are possible to be Executed
"""

import time

#
#   Define sub-functions which will be run if proper interrupt is made
#

def _int_21h_2(**kwargs):
    
    HR = kwargs["HR"]
    DL = int(HR.readFromRegister("DL"), 2)

    return {"write_char_to_terminal" : DL}

def _int_21h_44(**kwargs):
    """This interrupt stores current time in CX and DX in the following format:
    
    - CH - Hours
    - CL - Minutes
    - DH - Seconds
    - DL - Milliseconds
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

    HR = kwargs["HR"]
    max_length = HR.readFromRegister("DH")
    destination = HR.readFromRegister("DI")

    return {"terminal" : {
        "action" : "input_string_limited_width",
        "length" : max_length,
        "destination" : destination
    }}

#
#   Define function visible for the user
#

all_instructions = locals()

def INT(**kwargs):
    """
    # INTERRUPT
    ## Description
    This function performs system interruption. To perform interruption, proper value of
    interruption and arguments (AH and sometimes DL) must be specified. Calling proper
    interruption allows to execute action. Since this functionality is mostly crucial
    with actual interaction with machine, and it's quite complicated to implement
    while being trivial to understand (look up proper AH and INT values, set and execute)
    interrupt functionality was implemented in basic form, although allowing for further
    development for anyone interested. Depending on implementation, interrupt can do nothing
    or change quite a lot. 

    ## Supported operations
    ### 1. INT 21H, AH = 2   (2h)
    Write character which value is stored in DL. Doesn't change flags, nor registers.
    ### 2. INT 21H, AH = 44  (2Ch)
    Get current time in the operating system, and store it in CX and DX registers,
    putting:
    - CH - Hours
    - CL - Minutes
    - DH - Seconds
    - DL - Milliseconds
    ### 3. INT 21H, AH = 0   (0h)
    Terminate execution.
    ### 4. INT 21H, AH = 76  (4Ch)
    Terminate execution.
    ### 5. INT 21H, AH = 10  (Ah)
    Ask user for input with maximum specified length. At the time of calling, register
    DX must contain max length (DH) and location in memory (DL). Then user will be prompted
    to input text into terminal. Pressing Enter will confirmed input of the text, text
    will be stored in memory under the addres, and program will be contined.
    """

    HR = kwargs["HR"]
    AH = int(HR.readFromRegister("AH"), 2)

    hex_int_no = hex(kwargs["args_values_int"][0])[2:] + "h"
    interrupt = f"_int_{hex_int_no}_{AH}"

    specific_interrupt = all_instructions.get(interrupt, None)
    if not specific_interrupt:  return

    return specific_interrupt(**kwargs)

#
#   Assign params range and allowed params combination for functions
#

INT.params_range = [1]
INT.allowed_params_combinations = [ ("value",) ]
