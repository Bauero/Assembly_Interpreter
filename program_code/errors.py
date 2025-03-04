"""
This moduele holds all defined errors with it's definitions

Each error should contain it's own definition, with descriptio abot what hapened
which triggered en error
"""

from abc import abstractmethod

class DetailedException(Exception):
    """
    This is abstract class for methods which should rise specific exeption which
    could later be used to prompt user with warning
    """

    @abstractmethod 
    def line(self): ...

    @abstractmethod
    def message(self): ...



################################################################################
###     REGISTER ERRORS
################################################################################

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


################################################################################
###     FUNCTION ERROR
################################################################################


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

# TODO REMOVE
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

# TODO REMOVE
class TooManyArgumentsToUnpack (Exception):
    """
    This error is passed if funciton is run having passed too many params

    EX:

    'ADD     AX, BX, CX'

    'INC    AX, BX'
    """
    pass


class LabelNotRecognizedError (DetailedException):
    """
    This error occurs if label which is used in ex. jump, cannot be recognized.

    This can occur fe. if defined label is in different case than the one used
    while calling:
    
    Label1 != label1
    """

    def __init__(self, line_num = None, error_message = ""):
        self.error_message = error_message
        self.line_num = line_num

    def line(self):
        return self.line_num
    
    def message(self):
        return self.error_message

class ExecutionOfOperationInLineError (Exception):

    """
    This error is raised if some kind of error occured while processing a funciton.

    It's designed to be raised instead of each indivudal error, but contain the source
    error as paramether.
    """

    def __init__(self, exception : Exception):
        self.raised_exc = exception

    def __str__(self):
        return str(self.raised_exc)
    
    def __repr__(self):
        return self.raised_exc
    
    def source_exception(self):
        return self.raised_exc


class UnrecognizedArgumentInLineError(DetailedException):
    """This exception occurs when parsing line program cannot recognize what argument is
    passed in line. This can occur if user passes an incorrectly spelled label, var, improperly
    defined address, or there is something else which shouldn't be there"""
    
    def __init__(self, line_num = None, error_message = ""):
        self.error_message = error_message
        self.line_num = line_num

    def line(self):
        return self.line_num
    
    def message(self):
        return self.error_message


class KeywordNotImplementedError (DetailedException):
    """This error occurs if there is a keyword which is not recognized as one 
    supported by interpreter. Therefore it's either incorrect (ex. spelling mistake)
    or this interpreter simply doesn't know how to implement it"""
    
    def __init__(self, line_num = None, error_message = ""):
        self.error_message = error_message
        self.line_num = line_num

    def line(self):
        return self.line_num
    
    def message(self):
        return self.error_message
    

class IncorrectParamForBitMovError (DetailedException):
    """This error occurs if for one of the instruction: 
    
    SAL, SAR, SHL, SHR, ROL, ROR, RCL, RCR
    
    it is detected, that second argument is not allowed. FYI, if second argument
    is register it MUST BE 'cl' register"""

    def __init__(self, line_num = None, error_message = ""):
        self.error_message = error_message
        self.line_num = line_num

    def line(self):
        return self.line_num
    
    def message(self):
        return self.error_message

################################################################################
###     NUMBER ERROR
################################################################################


class WrongNumberBase (Exception):
    """
    This error means that system tried to read number as one in either binary, decimal or
    hexadecimal system, but the number didn't qualify as valid.
    """
    def __init__(self, message : str = ""):
        self.message = message

    def __str__(self):
        return self.message
    
    def __repr__(self):
        return self.__str__()


class NumberTooBig (Exception):
    """
    Provided number is too big for a given register

    ex.
    mov ah, 2987 (obviously, 8 bit register can't hold such a big number!)
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


class ValueIsNotANumber (Exception):
    """
    This error is raised if a number which should be converted to a given base
    raises error during conversion
    """
    
    def __init__(self, message = ""): self.message = message
    def __str__(self): return self.message


class IncorectValueInListOfBits (Exception):
    """
    This error is raised if program is asked to ensure that list containst values which
    suppose to be bits (like ['1', '1', '0']) but detects that one of the element is not
    '0' or '1'
    """
    
    def __init__(self, message = ""): self.message = message
    def __str__(self): return self.message


class NoExplicitSizeError (Exception):
    """
    This exceptin is raised if there is call to get data from address which is stored
    in register or as provided address in memory, but no size is specified - 
    therefore program doesn't know how much data to get from data:

    EX 1:
    MOV bx, var1
    MOV ax, [bx]    # bx, contains address of var 1 - but how many bits are stored in var1,
                    # this is undefined from the program perspective

    EX 2:
    MOV ax, [20h]
    """
    def __init__(self, message : str = ""):
        self.message = message

    def __str__(self):
        return self.message


################################################################################
###     FILE PROCESSING ERRORS
################################################################################


class ImproperJumpMarker (DetailedException):
    """
    This error is raised when program detects statemenet which seems to be a 
    marker for jump. Allowed loop names examples:

    - "JumpHere:" or "_Loop:" or "Loop1:"

    Examples of forbidden jump destination names:

    - "+:" or "   :" or "2x:"
    """
    def __init__(self, number : int | None = None, message : str = ""):
        self._message = message
        self._line_number = number

    def __str__(self):
        return str(self._line_number) + self._message
    
    def __repr__(self):
        return self.__str__()
    
    def line(self):     return self._line_number

    def message(self):  return self._message


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
    


################################################################################
###     DATA
################################################################################


class ImproperDataDefiniton (DetailedException):
    """
    This error is raised if during preprocessing of file a problem with reading data occurs.

    Data should be defined as:

    'Name Size Value' or 'Size Value' or 'Name Size v1, v2 ...' or Size v1, v2 ...'

    Allowed Sizes are: 'BYTE', 'DB', 'WORD', 'DW', 'DWORD', 'DD', 'QWORD', 'DQ'

    spaces between (optional) name, size and value (or values) are ignored. Values must be
    separated by coma ','.

    EX.

    - Good definion
    
    powit BYTE    "Witajcie w moich skromnych prograch :)", 0

    - Bad definion

    powit    "Witajcie w moich skromnych prograch :)", 0

    powit = "Witajcie w moich skromnych prograch :)", 0

    powit  8  "Witajcie w moich skromnych prograch :)", 0
    """
    def __init__(self, line_num : int | None = None, line_content : str = ''):
        # super().__init__()
        self._line_number = line_num
        self._line_content = line_content
    
    def __str__(self):
        return str(self._line_number) + self._line_content
    
    def __repr__(self):
        return self.__str__()
    
    def line(self):     return self._line_number

    def message(self):  return self._line_content


class SegmentationFault (Exception):
    """
    This error is raised if a call for data outside .data segment is made. 

    EX.

    *assume that this is the only data in .data*

    sum BYTE    "ALA" -> 3 bytes -> sum + 2 bytes

    Therefore:

    [sum+3] -> yields this error
    """
    ...


class ModificationOutsideDataSection (DetailedException):
    """
    This error is raise if user tires to modify data outside boundaries of data
    section
    """
    ...


class DataNotByteMultipleError (DetailedException):
    """
    This error is raised if, during saving data it is detected that value is stored
    in address which is not a multiple of 8 (doesn't fit in inter number of bytes). This
    is most likely a data storage error on the side of 
    """

    def __init__(self, message = "", line = None) -> None:
        self._message = message
        self._line = line

    def line(self):
        return self._line
    
    def message(self):
        return self._message




################################################################################
###     MEMORY ERRORS
################################################################################


class ImproperIndirectAddressingError (DetailedException):
    """
    This exceptions occurs when user tries to address value improperly:

    EX:

    [BX - SI] -> substraction not allowed; only addition is allowed
    """
    
    def __init__(self, message = "", line = None) -> None:
        self._message = message
        self._line = line

    def line(self):
        return self._line
    
    def message(self):
        return self._message
    
class DoubleMemoryCallError (DetailedException):
    """This exception occurs when in instruction there are two memory calls, which is
    illegal in x86 processors"""


################################################################################
###     OTHER ERRORS
################################################################################

class SizesDoesntMatchError(DetailedException):
    """This exception occurs when there is no match between sizes for variables as arguments
    in line.
    
    EX:
    
    var1 db 10
    
    ADD [var1], word 100    <- word doesn't fit in byte variable !!!
    """

    def __init__(self, message = "", line = None) -> None:
        self._message = message
        self._line = line

    def line(self):
        return self._line
    
    def message(self):
        return self._message

class NoExpliciteSizeDefinitionWhenRequiredError(DetailedException):
    """
    This error occurs when user doesn't specify size explicitly, therefore leaving comiler
    in state, when it doesn't know on how big range of memory it should operate.
    """

    def __init__(self, message = "", line = None) -> None:
        self._message = message
        self._line = line

    def line(self):
        return self._line
    
    def message(self):
        return self._message


################################################################################
###     OTHER ERRORS
################################################################################


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
