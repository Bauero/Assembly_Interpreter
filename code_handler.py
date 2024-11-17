"""
This file is responsible for managing opened file - loading it, and then passin instruction
to engine. It can communicate with engine to provide functionali like calling functions,
or jumps. It is also responible for managing history or operations done by program
"""

import os
from preprocessor import loadMainFile
from errors import FileDoesntExist, FileSizeMightBeTooBig, FileTypeNotAllowed


################################################################################
#   Global variables
################################################################################

allowed_file_types = ['.s','.asm']

################################################################################
#   Classes
################################################################################


class CodeHandler():
    """
    This class is responsible for handlind opened files - it passes lines for execution, 
    handles opened file and loades instruction for engine
    """

    def __init__(self, engine):
        self.openFiles = []
        self.fileExecLine = {}
        self.files = {}
        self.currentlyExecutedFile = ""
        self.engine = engine


    def loadFile(self, path_to_file, ignore_size_limit, ignore_file_type):
        raw_file = _loadFile(path_to_file, ignore_size_limit, ignore_file_type)
        assert type(raw_file) == list
        preprocessed_file = loadMainFile(raw_file)

        self.currentlyExecutedFile = path_to_file
        self.openFiles.append(path_to_file)
        self.files[path_to_file] = preprocessed_file
        



################################################################################
#   Functions variables
################################################################################


def _loadFile(path_to_file : str, 
              ignore_size_limit : bool = False,
              ignore_file_type : bool = False) -> list | Exception:
    """
    This function loads file (if one exist) and returns loaded file as subscribtable
    object for further processing.

    :param:
    - `ignore_size_limit` : bool - allow to process file above 1MB
    - `ignore_file_type` : bool - allow to process file with extenstion other than .s or .asm
    """

    if not os.path.exists(path_to_file):
        raise FileDoesntExist(path_to_file)
    elif not ignore_size_limit and os.path.getsize(path_to_file) > 1000000: # > 1MB
        raise FileSizeMightBeTooBig(path_to_file)
    elif not ignore_file_type and \
        (ext := os.path.splitext(path_to_file)[-1]) not in allowed_file_types:
        raise FileTypeNotAllowed(ext)

    raw_file = []

    with open(path_to_file) as file:
        for line in file:
            raw_file.append(line)

    return raw_file