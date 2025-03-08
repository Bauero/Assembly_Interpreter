"""
This file stores all instructions which are responsible for setting a specific flags in
procesor
"""

def CLC(**kwargs):
    """CLEAR CARRY FLAG - This instruction sets carry flag to 0"""

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
    """CLEAR DIRECTION FLAG - This instruction sets direction flag to 0"""
    
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
    """CLEAR INTERRUPT FLAG - This instruction sets interrupt flag to 0"""
    
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
    """COMPLEMENT CARRY FLAG - This instruction reverses value of carry flag"""
    
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
    """SET CARRY FLAG - This instruction sets carry flag to 1"""
    
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
    """SET DIRECTION FLAG - This instruction sets direction flag to 1"""
    
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
    """SET INTERRUPT FLAG - This instruction sets interrupt flag to 1"""
    
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

for fn_name in list(filter(lambda n: n.upper() == n, dir())):
    fn = locals()[fn_name]
    fn.params_range = [0]
    fn.allowed_params_combinations = [tuple()]
