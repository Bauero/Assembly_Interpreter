"""
This file contains non-critical 'errors' made by users - those shoudl be returned
to user in forms of warnings but are not sever enough to stop execution of thee
program
"""

class DetailedWarning(Warning):
    """Abstract-like klass whis one ensures that the class which inherits from it
    must have some methods initialized"""

    def __init__(self, *args):
        super().__init__(*args)

    def line(self): ...
    def message(self): ...
    def source_error(self): ...
    def solution(self): ...


class ExecutionOfOperationInLineWarning():
    
    def __init__(self, source_warning : DeprecationWarning, line : int):
        self.source_warning = source_warning
        self.warning_in_line = line

    def line(self): return self.warning_in_line
    def message(self): return self.source_warning.message()
    def source_error(self): return self.source_warning.source_error()
    def solution(self): return self.source_warning.solution()


################################################################################
###     Syntax Warningns
################################################################################

class ExpliciteSizeOperandIgnoredWarning(DetailedWarning):
    """This warning shows up when an explicite definiton of size doesn't cause an error
    but is explicitly ignored by compiler
    
    For example in this scenario:
    
    ADD [var3], byte Ax     <- putting 'byte' allows for comilation, but yields warining
    """

    def __init__(self, *args):
        super().__init__(*args)