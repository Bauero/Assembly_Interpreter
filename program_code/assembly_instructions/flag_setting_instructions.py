"""
This file stores all instructions which are responsible for setting a specific flags in
processor
"""

def CLC(**kwargs):
    """
    # CLEAR CARRY FLAG
    ## Description
    This instruction sets carry flag to 0. It doesn't affect any other flags.

    ## Summary
    CF = 0
    """

    FR  = kwargs["FR"]
    FR.setFlag("CF", 0)
    
    previous_state = FR.readFlags()
    new_state = FR.readFlags()

    response = {
        "action" :          "flags_changed",
        "location" :        "CF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

def CLD(**kwargs):
    """
    # CLEAR DIRECTION FLAG
    ## Description
    This instruction sets direction flag to 0. It doesn't affect any other flags.

    ## Summary
    DF = 0
    """
    
    FR  = kwargs["FR"]
    FR.setFlag("DF", 0)
    
    previous_state = FR.readFlags()
    new_state = FR.readFlags()

    response = {
        "action" :          "flags_changed",
        "location" :        "DF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

def CLI(**kwargs):
    """
    # CLEAR INTERRUPT FLAG
    ## Description
    This instruction sets interrupt flag to 0. It doesn't affect any other flags.

    ## Summary
    IF = 0
    """
    
    FR  = kwargs["FR"]
    FR.setFlag("IF", 0)
    
    previous_state = FR.readFlags()
    new_state = FR.readFlags()

    response = {
        "action" :          "flags_changed",
        "location" :        "IF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

def CMC(**kwargs):
    """
    # COMPLEMENT CARRY FLAG
    ## Description
    This instruction reverses value of carry flag. It doesn't affect any other flags.

    ## Summary
    CF != CF
    """
    
    FR  = kwargs["FR"]
    FR.setFlag("CF", not FR.readFlag("CF"))
    
    previous_state = FR.readFlags()
    new_state = FR.readFlags()

    response = {
        "action" :          "flags_changed",
        "location" :        "CF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

def STC(**kwargs):
    """
    # SET CARRY FLAG
    ## Description
    This instruction sets carry flag to 1. It doesn't affect any other flags.

    ## Summary
    CF = 1
    """
    
    FR  = kwargs["FR"]
    FR.setFlag("CF", 1)
    
    previous_state = FR.readFlags()
    new_state = FR.readFlags()
    
    response = {
        "action" :          "flags_changed",
        "location" :        "CF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

def STD(**kwargs):
    """
    # SET DIRECTION FLAG
    ## Description
    This instruction sets direction flag to 1. It doesn't affect any other flags.

    ## Summary
    DF = 1
    """
    
    FR  = kwargs["FR"]
    FR.setFlag("DF", 1)
    
    previous_state = FR.readFlags()
    new_state = FR.readFlags()
    
    response = {
        "action" :          "flags_changed",
        "location" :        "DF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

def STI(**kwargs):
    """
    # SET INTERRUPT FLAG
    ## Description
    This instruction sets interrupt flag to 1. It doesn't affect any other flags.

    ## Summary
    IF = 1
    """
    
    FR  = kwargs["FR"]
    FR.setFlag("IF", 1)
    
    previous_state = FR.readFlags()
    new_state = FR.readFlags()
    
    response = {
        "action" :          "flags_changed",
        "location" :        "IF",
        "modified_type" :   "flag_register",
        "oryginal_value" :  list(previous_state),
        "new_value" :       list(new_state)
    }

    return response

#
#   Assign params range and allowed params combination for functions
#

for fn in [CLC, CLD, CLI, CMC, STC, STD, STI]:
    fn.params_range = [0]
    fn.allowed_params_combinations = [tuple()]
