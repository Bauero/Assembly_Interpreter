"""
This file contains functions which purpose is to read, and preprocess file to 
allow for it's further use inside program.
"""

import re
from .hardware_memory import DataSegment
from .helper_functions import (return_size_from_name,
                               return_if_base_16_value,
                               return_if_base_10_value,
                               return_if_base_8_value,
                               return_if_base_2_value,
                               return_size_from_name)
from .errors import ImproperJumpMarker, ImproperDataDefiniton

def loadMainFile(raw_file : list, Data : DataSegment) -> tuple:
    """
    This function tries to read and load file specified in the path - this is main funciton
    responsible for reading code - executing it with success, shoudl allow to run code from
    file.
    """

    assembly_code = _initialLoadAndCleanup(raw_file, Data)
    assembly_code = _divideCodeToSection(assembly_code)
    assembly_code = _replaceEquateValues(assembly_code)
    assembly_code = _replaceTimesValues(assembly_code)
    # assembly_code = _replaceCharWithInt(assembly_code)
    # assembly_code = _replaceDUPValues(assembly_code)
    # assembly_code = _wrapMultiLineData(assembly_code)
    assembly_code = _storeVariablesInData(assembly_code)
    
    start = _decideWhereExecutioinStarts(assembly_code)

    return start, assembly_code

def _initialLoadAndCleanup(file : list, Data : DataSegment):
    """
    Remove comments and empty lines - ignore directives and secitons
    """
    
    allowed_sections = ['code', 'stack', 'data', 'text']

    assembly_code = {
        'lines' : [],
        'labels' : {},
        'variables' : {},
        'data' : Data
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
        if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:", line):
            values = line.split(':')
            assert len(values) > 0, 'Empty ":" in line - did you forget the identifier?'
            
            if not ' ' in values[0]:
                assert len(values) < 3, 'Multiple ":" in one line detected'
                marker_in_line, line = values
                
        #   Detect imporper line with ":"
        if re.match(r"(?<!\S)(\d\w*:|[^a-zA-Z_][\w]*:|[a-zA-Z_]\w*[^a-zA-Z0-9_\s]+.*:|:\s.*)", line):
            raise ImproperJumpMarker(number, f"\nIncorrect line with \":\" -> [{line}]'")

        #   Save results
        if marker_in_line:
            assembly_code['labels'][marker_in_line] = len(assembly_code['lines'])
            continue
        
        assembly_code['lines'].append(
            {
                "lines" : [number],
                "marker": marker_in_line,
                "content": line
            }
        )
    
    return assembly_code

def _divideCodeToSection(assembly_code : list):
    """
    This command will limit the subset of lines in code for execution, by spliting code
    into sections. This is done to allow for initial preprocessing of functions and
    variables
    """

    default_section = ".code"
    current_section = default_section
    alaius = True # all lines are in undefined section

    for id, line in enumerate(assembly_code['lines']):
        content = line['content']
        if content.lower().startswith("section"):
            content = content[7:] # 7 is the length of 'section'
        line_beginning = content.strip().split(" ")[0].lower()

        match line_beginning:
            case '.code':           current_section = ".code";      alaius = False
            case '.data':           current_section = ".data";      alaius = False
            case '.text':           current_section = ".code";      alaius = False
            case '_':               current_section = '.code'
        
        assembly_code['lines'][id]["section"] = current_section

    # If all lines are undefined, therefore file contains only code section
    if alaius:
        for id, line in enumerate(assembly_code['lines']):
            assembly_code['lines'][id]["section"] = '.code'

    return assembly_code

def _replaceEquateValues(assembly_code : list):
    """
    This function looks for lines with 'EQU' macro, which allows for replacement of values
    within code with values provided to the macro. 
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
            does_it_match = re.search(filter_pattern(name), content)
            if does_it_match:
                symbol_value[name]['matches'] += 1
            if symbol_value[name]['matches'] > 1:
                output = re.sub(filter_pattern(name), symbol_value[name]['number'], content)
                assembly_code['lines'][id]['content'] = output

    return assembly_code

def _replaceTimesValues(assembly_code : list):
    """This funciton replaces values which are multiplied using `times` directive.
    ```
    INPUT:      var times 4 db "Value"
    OUTPUT:     var db "ValueValueValueValue"
    ```
    """
    
    def split_assembly_line(line):
        pattern = r'([^\s"\']+)|(["\'])(.*?)(\2)'
        tokens = [match[0] if match[0] else match[2] for match in re.findall(pattern, line)]
        return tokens

    pattern = r"(?i)^\s*times\s+\d+\s+(db|dw|dd|dq)\s+(['\"]).*?\2\s*$"

    data_rows = [no for no, line in enumerate(assembly_code['lines']) if line['section'] == ".data"]

    for id in data_rows:
        content = assembly_code['lines'][id]['content']
        matched = re.search(pattern, content)
        if matched:
            start   = matched.start()
            value   = matched.group()

            _, rep, size, text = split_assembly_line(value)
            rep = int(rep)
            text = text * rep
            new_line = content[:start] + size + " " + text
            assembly_code['lines'][id]['content'] = new_line

    return assembly_code

def _replaceCharWithInt(assembly_code : list):
    """This function parses values in code, and substitues each """
    
    
    ...

def _replaceDUPValues(assembly_code : list):
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
        matched = re.search(pattern, content)
        
        if matched:
        
            start   = matched.start()
            end     = matched.end()
            value   = matched.group()

            repeat, _, what = value.split(" ")
            new_line_part = "".join((what[1:-1] for _ in range(int(repeat))))
            assembly_code['lines'][id]['content'] = content[:start] + new_line_part + content[end:]

    return assembly_code

def _wrapMultiLineData(assembly_code : list):
    """
    This function would 'unwrap' multiline data definitions
    ### EX:
    ```
    example BYTE    "Line 1", cr, Lf,
                    "Line 2", cr, Lf,
                    "Line 3"
    ```
    will be transformed to:
    ```
    example BYTE    "Line 1", cr, Lf, "Line 2", cr, Lf, "Line 3"
    ```
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

def _storeVariablesInData(assembly_code : list):
    """
    This function converts values from data section, to variables in Data
    """

    data_rows = [no for no, line in enumerate(assembly_code['lines']) if line['section'] == ".data"]
    byte_counter = 0

    for i in data_rows:
        line = assembly_code['lines'][i]['content']

        #   If line starts with segment directive, check if there is anything else in that
        # line if we remove segment directive - if not skip it
        if line.lower() in [".data", "section .data"]:
            continue

        line_split = [a for a in line.split(" ") if a]  #   -> Divide, and remove spaces
        allowed_data_types = ['DB', 'DW', 'DD', 'DQ']

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

        storage_size = return_size_from_name(dtt)   # 8, 16, 32 etc. bits

        starting_address = byte_counter
        elements = []
        tmp = ''
        inside_text = False

        for char in var_content:
            if not inside_text and char == '"':
                inside_text = True
                tmp += char
            elif inside_text and char == '"':
                inside_text = False
                tmp += char
                elements.append(tmp)
                tmp = ''
            elif not inside_text and char == ',':
                if not tmp:
                    continue
                elements.append(tmp)
                tmp = ''
            else:
                tmp += char
        else:
            elements.append(tmp)

        for element in elements:
            is_text = False
            element = str(element).strip() if type(element) != str else element
            if element.startswith('"') and element.endswith('"'):
                element = element[1:-1]
                is_text = True

            if element == "?":
                [str(0) for _ in range(storage_size)]
                for e in range(storage_size):
                    assembly_code['data'].modify_data(byte_counter, 0)
                continue

            elif not is_text:
                element = element.strip()

                if value := return_if_base_16_value(element):       base = 16
                elif value := return_if_base_10_value(element):     base = 10
                elif value := return_if_base_8_value(element):      base = 8
                elif value := return_if_base_2_value(element):      base = 2

                if bool(value):
                    bite_list = bin(int(element, base))[2:].zfill(storage_size)
                    byte_counter =  assembly_code['data'].modify_data(byte_counter, bite_list)
                    continue

            for c in element:
                bite_list =  bin(ord(c))[2:].zfill(storage_size)
                byte_counter = assembly_code['data'].modify_data(byte_counter, bite_list)

        start_add, size = starting_address , byte_counter - starting_address

        #   If data have a name, store it with address, size and format
        if var_name:
            assembly_code['variables'][var_name] = {    # data : "ala"   # data : 68   # data : "Mati"
                'address'   : start_add,                # 0              # 3           # 4
                'size'      : size,                     # 3 (bytes)      # 1           # 8 (4 * 16 bits = 8 bytes)
                'format'    : storage_size              # 8 (bits)       # 8 (bits)    # 16 bits
            }

    return assembly_code

def _decideWhereExecutioinStarts(assembly_code : dict) -> tuple:
    """
    This function analyzes the code which is stored in variable assembly_code
    and makes decision where to start the code. I assume that the execution starts
    in 2 different scenarios:

    1. At the "start" label, and if one is not present
    2. At the first line which is not empty, doesn't contain comment, and belongs
    to .code section
    """

    # Case 1
    for label in assembly_code['labels']:
        if label.lower().endswith('start'):
            line_number = assembly_code['labels'][label]
            if assembly_code['lines'][line_number]['section'] == '.code':
                return (line_number, assembly_code['lines'][line_number]['lines'])
    
    # Case 2
    for n, line in enumerate(assembly_code['lines']):
        if line['section'] == '.code':
            if line['content'].lower() in [".code", "section .code"]:
                continue
            elif line['content'].lower().split(" ")[0] == "org":
                continue
            else:
                return n, line['lines']
        
    # No code to execute
    return -1, [-1]
