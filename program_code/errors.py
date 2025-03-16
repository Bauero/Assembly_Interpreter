"""
This module holds all defined errors with it's definitions

Each error should contain it's own definition, with description about what happend
which triggered en error
"""

class DetailedException(Exception):
    """
    This is abstract class for methods which should rise specific exception which
    could later be used to prompt user with warning
    """

    def __init__(self, name : str, line : int | None = None, param_no : int | None = None, 
                   params : list | None = None, values : str | None = None, 
                   exc : Exception | None = None):
        
        self.name = name
        self.line = line
        self.param_no = param_no
        self.params = params
        self.values = values
        self.exc = exc

    def get_details(self):
        return {
            "popup" : self.name,
            "line" : self.line,
            "param_no" : self.param_no,
            "params" : self.params,
            "values" : self.values,
            "source_error" : self.exc
        }


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


class WrongNumberBase (DetailedException):
    """
    This error means that system tried to read number as one in either binary, decimal or
    hexadecimal system, but the number didn't qualify as valid.
    """
    pass

class ValueIsNotANumber (Exception):
    """
    This error is raised if a number which should be converted to a given base
    raises error during conversion
    """
    pass


class IncorectValueInListOfBits (Exception):
    """
    This error is raised if program is asked to ensure that list contains values which
    suppose to be bits (like ['1', '1', '0']) but detects that one of the element is not
    '0' or '1'
    """
    pass


################################################################################
###     FILE PROCESSING ERRORS
################################################################################


class ImproperJumpMarker (DetailedException):
    """
    This error is raised when program detects statement which seems to be a 
    marker for jump. Allowed loop names examples:

    - "JumpHere:" or "_Loop:" or "Loop1:"

    Examples of forbidden jump destination names:

    - "+:" or "   :" or "2x:"
    """
    pass

class ImproperVariableName (DetailedException):
    """
    This error is generated when a variable with improper name is declared
    """
    pass


class FileDoesntExist (Exception):
    """
    This error is raised if user tries to pass path to file which doesn't exist
    """
    pass


class FileSizeMightBeTooBig (Exception):
    """
    This error is raise if file which is opened is too big (above 1MB). It is
    to prevent opening files which would force interpreter to use extended resource.

    It can be omitted if needed.
    """
    pass


class FileTypeNotAllowed (Exception):
    """
    This error is raised if during processing a file with not allowed extension
    is passed for processing
    """
    pass


class EmptyFileError (Exception):
    """
    This error is raised if during processing an empty file, or one containing only white
    characters is passed for processing
    """
    pass


################################################################################
###     DATA
################################################################################


class ImproperDataDefiniton (DetailedException):
    """
    ## Description
    This error is raised if during preprocessing of file a problem with reading data occurs.
    Data should be defined as:
    - 'Name Size Value' or 'Size Value' or 'Name Size v1, v2 ...' or Size v1, v2 ...'
    
    Allowed Sizes are: 'BYTE', 'DB', 'WORD', 'DW', 'DWORD', 'DD', 'QWORD', 'DQ'. 
    Spaces between (optional) name, size and value (or values) are ignored. Values must be
    separated by coma ','.

    ## EX.

    ### Good definition
    - hello BYTE    "Good morning", 0

    ### Bad definition
    - hello    "Good morning", 0
    - hello = "Good morning", 0
    - hello  8  "Good morning", 0
    """
    pass


class SegmentationFault (Exception):
    """
    ## Description
    This error is raised if a call for data outside .data segment is made. 

    ## EX.
    *assume that this is the only data in .data*
    - sum BYTE    "ALA" -> 3 bytes -> sum + 2 bytes

    ### Therefore:
    - [sum+3] -> yields this error
    """
    pass


class ModificationOutsideDataSection (DetailedException):
    """
    This error is raise if user tires to modify data outside boundaries of data
    section
    """
    pass
