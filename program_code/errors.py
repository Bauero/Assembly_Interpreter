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


class ImproperVariableName (DetailedException):
    """
    This error is generated when a variable with improper name is declared
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
