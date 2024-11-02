"""
This file contains code which is reponsible for magement of assembly code which is being
read, processed, executed.
"""
import os
from re import match
from errors import FileDoesntExist, ImproperJumpMarker, FileSizeMightBeTooBig, \
                   FileTypeNotAllowed

assembly_code = {
    'lines' : [],
    'labels' : [],
    'variables' : {}
}

def loadMainFile(path_to_file : str, 
                 ignore_size_limit : bool = False,
                 ignore_file_type : bool = False) -> None | Exception:
    """
    This function tries to read and load file speciphied in the path - this is main funciton
    responsible for reading code - executing it with success, shoudl allow to run code from
    file.
    """

    allowed_file_types = ['.s','.asm']

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

    cleanAndProcessFile(raw_file)
    

def cleanAndProcessFile(file : list):
    """
    Remove comments and empty lines - ignore directives and secitons
    """

    global assembly_code

    for number, line in enumerate(file, 1):

        marker_in_line = None

        #   Remove comments and empty lines
        line = line.split(";")[0]
        line = line.strip()
        if len(line) < 1:   continue

        #   Detect indentifiers (points where code could jump to)
        if match("^[a-zA-Z_][a-zA-Z0-9_]*:", line):
            values = line.split(':')
            assert len(values) > 0, 'Empty ":" in line - did you forget the identifier?'
            
            if not ' ' in values[0]:
                assert len(values) < 3, 'Multiple ":" in one line detected'
                marker_in_line, line = values
                
        #   Detect imporper line with ":"
        if match("(?<!\S)(\d\w*:|[^a-zA-Z_][\w]*:|[a-zA-Z_]\w*[^a-zA-Z0-9_\s]+.*:|:\s.*)", line):
            raise ImproperJumpMarker(f"\nIncorrect line with \":\" -> [{line}]'")


        #   Save results
        if marker_in_line:
            assembly_code['labels'].append(marker_in_line)
        
        assembly_code['lines'].append(
            {
                "lines" : [number],
                "marker": marker_in_line,
                "content": line
            }
        )
        
