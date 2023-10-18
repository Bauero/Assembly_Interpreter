"""
This moduele holds all defined errors with it's definitions
"""

###     REGISTER ERRORS

class RegisterNotImplemented (Exception): 
    """
    This error occurs when you try to call an operation on non existing register
    """
    pass

class RegisterTooSmallToMove (Exception): 
    """
    This errro occurs when you try to perform move operation on registers
    which is too small to hold the value

    ex.
    mov ah,ax
    """
    pass


class RegisterSizeTooSmall (Exception):
    """
    This error occurs when you try to move value to the register which is not
    big enough to hold the value

    ex.
    mov ah, 300
    """
    pass

class OperationNotPossible (Exception):
    """
    This error occurs when you try to perform an operation which is not
    possible due to architecture limitation of 16-bit assebly programming

    ex. 
    - mov [variable1],[variable2] # operation from memory to memoery directly
    """
    pass

class RegisterCantEffectiveAddress (Exception):
    """
    It is not possible to get the effective address from the register

    In most cases it meant, that you tried to store and access value of
    a variable from register which can't allow that (architecture reasons)

    As a reminder - you can only get effective address of a variable from
    DX(DH/DL) or BX(BH/BL) registers
    """
    pass

class RegisterNotWritable (Exception):
    """
    This error occurs when you try to write something to register which is not
    ment to be written to

    In 16-bit assembly it is `sp` register (stack pointer register)
    """
    pass

###     NUMBER ERROR

class WrongNumberBase (Exception):
    """
    To be implemented later
    """
    pass

class NumberTooBig (Exception):
    """
    Provided number is too big for a given register

    ex.
    mov ah,2987 (obviously, 8 bit register can't hold such a big number)
    """
    pass

class NumberSizeRequired (Exception):
    """
    This error indicated that you have to explicitly provide size
    of the number - dw, dt, word etc.
    """
    pass

class CantPushValueTooBig (Exception):
    """
    This error indicates that you are trying to push value greater
    than 16 bit onto stack
    """
    pass

###     OTHER ERRORS

class OperandSizeNotSpecified (Exception):
    """
    This error indicated that you have to explicitly provide size
    of the operation - dw, dt, word etc.
    """
    pass

class EffectiveAddressError (Exception):
    """
    This error indicated that you propably misspelled hence program
    couldn't understant how paranthesis should be read
    """
    pass

class EffectiveAddresNotExist (Exception):
    """
    This error indicates, that the effective address you are trying to access
    does not exist - this doesn't have to be prohibited in the assembly itslef,
    but it's unsafe it's rather a mistake than an expected behaviour
    """
    pass

class VariableAddressNotExisting (Exception):
    """
    This error indicated that you used name of variable which is not
    defined - propably a writing mistake
    """
    pass
