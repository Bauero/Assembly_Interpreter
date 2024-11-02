"""
This moduele holds all defined errors with it's definitions

Each error should contain it's own definition, with descriptio abot what hapened
which triggered en error
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

###     FUNCTION ERROR

class EmptyLine (Exception):
    """
    This error occurs when there is an empty line

    Although, technicly, en error, this one is rather to be
    later use by program, to internally deal with empty lines in file

    IMPORTANT:
    As an empty line we categorize each line, which does not contain
    actual code - this include both lines with comments only and 'physically'
    empty lines in file

    EX - each line would raise error:

    1. '                    '

    2. ' ;ajsjaslkaj        '

    3. ''
    """
    pass

class ArgumentNotExpected (Exception):
    """
    This error occurs if function tried to be executed while not needing
    any parametres

    EX:
    PUSHA   DX <- this is not needed here, so this error would be raised
    """
    pass

class NotEnoughArguments (Exception):
    """
    This error is raised, if function tries to be executed, while not having
    enough parametres passed

    EX:
    
    'ADD     AX,'

    'ADD     '

    'ADD'
    """
    pass

class TooManyArgumentsToUnpack (Exception):
    """
    This error is passed if funciton is run having passed too many params

    EX:

    'ADD     AX, BX, CX'

    'INC    AX, BX'
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


###     FILE PROCESSING ERRORS

class ImproperJumpMarker (Exception):
    """
    This error is raised when program detects statemenet which seems to be a 
    marker for jump. Therefore instead of construction like:

    - "JumpHere:" or "_Loop:" or "Loop1:"

    is encounters:

    - "+:" or "   :" or "2x:"
    """
    def __init__(self, message = ""): self.message = message
    def __str__(self):  return self.message
    
class FileDoesntExist (Exception):
    """
    This error is raised if user tries to pass path to file which doesn't exist
    """

    def __init__(self, message = ""): self.message = message
    def __str__(self): return f"file {self.message} doesn't exist"


class FileSizeMightBeTooBig (Exception):
    """
    This error is raise if file which is beign open is too big (above 1MB). It is
    to prevent opening files which would force interpreter to use extended resource.

    It can be ommited if needed.
    """
    def __init__(self, message = ""): self.message = message
    def __str__(self): return f"file {self.message} too big"


class FileTypeNotAllowed (Exception):
    """
    This error is raised if during processing a file with not allowed extension
    is pased for processing
    """

    def __init__(self, extension = "", allowed = ['.s','.asm']):
        self.message = extension
        self.allowed = allowed
    def __str__(self):
        return f"extension {self.message} not allowed - allowed extnsions: {self.allowed}"
    

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
