"""
This file contains functions which purpose is to read, and preprocess file to 
allow for it's further use inside program.
"""
import os
from re import match, search, sub
from datatypes import Data
from helper_functions import return_size_from_name
from errors import ImproperJumpMarker, ImproperDataDefiniton

################################################################################
#   Global variables
################################################################################

allowed_sections = ['code', 'stack', 'data', 'text']

################################################################################
#   Public functions
################################################################################


def loadMainFile(raw_file : list) -> dict | Exception:
    """
    This function tries to read and load file speciphied in the path - this is main funciton
    responsible for reading code - executing it with success, shoudl allow to run code from
    file.
    """

    assert type(raw_file) == list

    assembly_code = _initialLoadAndCleanup(raw_file)
    assembly_code = _divideCodeToSection(assembly_code)
    assembly_code = _replaceEquateValues(assembly_code)
    assembly_code = _replaceDUPValues(assembly_code)

    assert assembly_code != None
    
    assembly_code = _wrapMultiLineData(assembly_code)
    assembly_code = _storeVariablesInData(assembly_code)

    return assembly_code
    

################################################################################
#   Private functions
################################################################################


def _initialLoadAndCleanup(file : list):
    """
    Remove comments and empty lines - ignore directives and secitons
    """

    assembly_code = {
        'lines' : [],
        'labels' : [],
        'variables' : {},
        'data' : Data()
    }

    for number, line in enumerate(file, 1):

        marker_in_line = None

        #   Remove comments and empty lines
        line = line.split(";")[0]
        line = line.strip()
        if len(line) < 1:   continue

        #   Skip any 'seciton header' which will not be processed
        if line.startswith('.') and line[1:].split(" ")[0].lower() not in allowed_sections:
            continue

        #   Detect indentifiers (points where code could jump to)
        if match("^[a-zA-Z_][a-zA-Z0-9_]*:", line):
            values = line.split(':')
            assert len(values) > 0, 'Empty ":" in line - did you forget the identifier?'
            
            if not ' ' in values[0]:
                assert len(values) < 3, 'Multiple ":" in one line detected'
                marker_in_line, line = values
                
        #   Detect imporper line with ":"
        if match("(?<!\S)(\d\w*:|[^a-zA-Z_][\w]*:|[a-zA-Z_]\w*[^a-zA-Z0-9_\s]+.*:|:\s.*)", line):
            raise ImproperJumpMarker(number, f"\nIncorrect line with \":\" -> [{line}]'")

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
    
    return assembly_code
        

def _divideCodeToSection(assembly_code):
    """
    This command will limit the subset of lines in code for execution, by spliting code
    into sections. This is done to allow for initial preprocessing of functions and
    variables
    """

    default_section = "undefined"
    current_section = default_section
    alaius = True # all lines are in undefined section

    for id, line in enumerate(assembly_code['lines']):
        content = line['content']
        if content.lower().startswith("section"):
            content = content[7:] # 7 is the length of 'section'
        line_beginning = content.strip().split(" ")[0].lower()

        match line_beginning:
            case '.code':           current_section = ".code";      alaius = False
            case '.stack':          current_section = ".stack";     alaius = False
            case '.data':           current_section = ".data";      alaius = False
            case '.text':           current_section = ".code";      alaius = False
            case '_':               current_section = 'undefined'
        
        assembly_code['lines'][id]["section"] = current_section

    # If all lines are undefined, therefore file contains only code section
    if alaius:
        for id, line in enumerate(assembly_code['lines']):
            assembly_code['lines'][id]["section"] = '.code'

    return assembly_code

                
def _replaceEquateValues(assembly_code):
    """
    This function looks for lines with 'EQU' macro, which allows for replacement of values
    within kode with values provided to the macro. 
    """

    undefined_lines = filter(lambda l: l['section'] == 'undefined', assembly_code['lines'])
    symbol_value = {}

    for line in undefined_lines:
        line = list(filter(lambda x: x > "", line['content'].split(" ")))
        if len(line) == 3 and line[1].lower() == 'equ':
            symbol_value[line[0]] = {
            'number' : line[2],
            'matches' : 0
        }

    #   if no values were found for replacement end funciton here
    if not symbol_value:    return  assembly_code
    
    filter_pattern = lambda x: fr'(?<!["\'])(\b{x}\b)(?!["\'])'

    for id in range(len(assembly_code['lines'])):
        
        for name in symbol_value:
        
            content = assembly_code['lines'][id]['content']
            does_it_match = search(filter_pattern(name), content)
            if does_it_match:
                symbol_value[name]['matches'] += 1
            if symbol_value[name]['matches'] > 1:
                output = sub(filter_pattern(name), symbol_value[name]['number'], content)
                assembly_code['lines'][id]['content'] = output

    return assembly_code


def _replaceDUPValues(assembly_code):
    """
    Within .data section it is possible to define variable with 'DUP' directive which 
    will duplicate value provided within paranthesis:

    EX.

    10 DUP (*) -> **********
    """

    #   Filter values like "number DUP (some_value)"
    pattern = r"\b\d+\s+[dD][uU][pP]\s*\(\s*([\da-fA-F]+|\?|[a-zA-Z]|\W)\s*\)"
    
    #   Filter all rows with data
    data_rows = [no for no, line in enumerate(assembly_code['lines']) if line['section'] == ".data"]

    for id in data_rows:
        
        content = assembly_code['lines'][id]['content']
        matched = search(pattern, content)
        
        if matched:
        
            start   = matched.start()
            end     = matched.end()
            value   = matched.group()

            repeat, _, what = value.split(" ")
            new_line_part = ",".join((what[1:-1] for _ in range(int(repeat))))
            assembly_code['lines'][id]['content'] = content[:start] + new_line_part + content[end:]

    return assembly_code


def _wrapMultiLineData(assembly_code):
    """
    This function would 'unwrap' multiline data definitions

    EX:
    example BYTE
    "Line 1", cr, Lf,
                    
    "Line 2", cr, Lf,
    
    "Line 3"
    
    will be transformed to:

    example BYTE    "Line 1", cr, Lf, "Line 2", cr, Lf, "Line 3"

    """

    inside_multiline = False
    all_lines = []
    current_multiline = []
    data_rows = [no for no, line in enumerate(assembly_code['lines']) if line['section'] == ".data"]

    #   Analyze which lines are multiline, and which lines belongs to one variable
    for row in data_rows:
        if assembly_code['lines'][row]['content'].strip().endswith(','):
            if inside_multiline:
                current_multiline.append(row)
            else:
                current_multiline.append(row)
                inside_multiline = True
        else:
            if inside_multiline:
                current_multiline.append(row)
                all_lines.append(current_multiline)
                current_multiline = []
                inside_multiline = False
            else:
                all_lines.append([row])

    lines_to_remove = []

    #   Add content from other lined to the first line, and mark other lines for removal
    for ml in filter(lambda l: len(l) > 1, all_lines):
        main_line, *other_lines = ml
        for l in other_lines:
            assembly_code['lines'][main_line]['content'] += \
                assembly_code['lines'][l]['content'].strip()
            assembly_code['lines'][main_line]['lines'].append(
                assembly_code['lines'][l]['lines'][0]
            )
        lines_to_remove.extend(other_lines)

    #   Remove lines with content which was moved to first line of multiline variable
    for l in range(len(lines_to_remove)-1, -1, -1):
        assembly_code['lines'].pop(lines_to_remove[l])

    return assembly_code


def _storeVariablesInData(assembly_code):
    """
    This function converts values from data section, to variables in Data
    """

    data_rows = [no for no, line in enumerate(assembly_code['lines']) if line['section'] == ".data"]

    for i in data_rows:
        line = assembly_code['lines'][i]['content']

        #   If line starts with segment directive, check if there is anything else in that
        # line if we remove segment directive - if not skip it
        if line.upper().startswith('.DATA'):
            if not [l for l in line[5:].split(' ') if l]:
                continue

        line_split = [a for a in line.split(" ") if a]  #   -> Divide, and remove spaces
        allowed_data_types = ['BYTE', 'DB', 'WORD', 'DW', 'DWORD', 'DD', 'QWORD', 'DQ']

        end_of_dtt_in_line = 0
        dtt = ''
        var_name = ''

        #   Check if line contains name for data, separate optional name and storage size
        # (ex. BYTE) by checking where to slice line
        try:
            if line_split[0].upper() in allowed_data_types:
                dtt = line_split[0]
                end_of_dtt_in_line = line.find(dtt) + len(dtt)
            elif line_split[1].upper() in allowed_data_types:
                var_name = line_split[0]
                dtt = line_split[1]
                end_of_dtt_in_line = line.find(dtt) + len(dtt)
        except Exception:
            raise ImproperDataDefiniton(i + 1, line)
        
        #   Slice line:     {v1 BYTE "A","B"} -> {"A","B"}
        var_content = line[end_of_dtt_in_line:].strip()

        storage_size = return_size_from_name(dtt)

        #   Write data, and receive it's size in data section
        start_add, size = assembly_code['data'].add_data(storage_size, var_content)

        #   If data have a name, store it with address, size and format
        if var_name:
            assembly_code['variables'][var_name] = {
                'address'   : start_add,
                'size'      : size,
                'format'    : storage_size
            }

    return assembly_code
