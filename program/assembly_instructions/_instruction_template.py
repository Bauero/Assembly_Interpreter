"""
This file contains template of the instruction which can be used to develop new functionality

It is must use the
"""

##################################   INFO 1   ##################################

# Function have to accept 3 parameters - regardless of how many are used within it
# Names are speciphied - in cace of problems understanding, search project
# for files hardware_registers.py and flag_register.py

# from hardware_registers import HardwareRegisters
# from flag_register import FlagRegister
# from hardware_memory import DataSegment

##################################   INFO 2   ##################################

# IMPORTANT! - name MUST BE only capital letters (technically .isupper() must return "true")
# as this code automatically detects functions based on it's naming scheme

# def EXAMPLE(HardwareRegister : HardwareRegisters, 
#               FlagRegister : FlagRegister,
#               Data : DataSegment,
#               *params):
#     """This function performs addition"""

##################################   INFO 3    ##################################

#       This attribute must be speciphied as it will be used to determine if passed
#   paramethers match the signature
# 
#     EXAMPLE.__setattr__('params_range', [2])    
#
#               *your code here*
# 

##################################   INFO 4    ##################################

#   It is necessary to return oryginal arguments after code inside funciton is executed.
#   

#     return HardwareRegister, FlagRegister, Data