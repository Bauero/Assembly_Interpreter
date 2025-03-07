"""
This file contains Engine Class, which is responsible for simluation of operations on memory
"""

from inspect import signature
from simpleeval import simple_eval
from .assembly_instructions import *
from .helper_functions import *
from .hardware_memory import DataSegment
from .hardware_registers import HardwareRegisters
from .flag_register import FlagRegister
from .custom_message_boxes import *

allowed_data_types = ['BYTE', 'WORD', 'DWORD', 'QWORD']

class Engine():
    """
    This class is responsible for execution of instructions within program. It has access
    to virutal hardware, and given the instruction, it executes it, and modifies the registers
    and flags accordingly
    """

    def __init__(self, language : str):
        self._prepareFunctions()
        self.HR = HardwareRegisters()
        self.FR = FlagRegister()
        self.data = DataSegment()
        self.variables = []
        self.language = language

    def informAboutLabels(self, labels : list):
        """This method allow to pass labels to engine after successful preprocessing"""
        self.labels = labels

    def informAboutVariables(self, variables : list):
        """This method allow to pass variables to engine after successful preprocessing"""
        self.variables = variables

    def set_language(self, new_language : str):
        """This method allow to pass language setting to engine - for warnings/errors"""
        self.language = new_language

    def executeInstruction(self, line : int, command : str):
        """This function is responsible for command execution - it cuts the line, extracting command
        from arguments, defines what types are the arguments, defines what they represent, and passes
        so prepared elements to _functionExecutor()"""
        
        self.curr_line = line
        elements_in_line = []

        keyword, first_non_keyw_char = self._separate_keyword(command)
        if keyword not in self.funtionNameLink:
            unsuported_instruction(self.language)
            return -1
        
        elements_in_line.append(keyword)
        arguments = command[first_non_keyw_char:].strip().split(",")
        arguments = [arg.strip() for arg in arguments if arg]
        elements_in_line.extend(arguments)

        explicite_sizes, arguments_no_size = self._extract_explicite_size_def(arguments)
        args_cleaned = list(map(lambda x: x.strip(), arguments_no_size))

        args_types = self._detect_argument_type(args_cleaned)
        if "undefined" in args_types:
            unrecognized_argument(self.language, self.curr_line + 1)
            return -1

        args_checked = self._check_validity_of_arguments_return_stadardized(args_cleaned, 
                                                                            args_types)
        if args_checked == None:
            return -1
        
        extracted = self._extract_argument_value_and_size(args_checked, args_types, 
                                                          explicite_sizes)
        args_values_raw, args_values_int, final_sizes, destination = extracted
        
        for i, arg in enumerate(args_types):
            if arg == "complex value":      args_types[i] = "value"
            elif arg == "memory call":      args_types[i] = "memory"

        final_standardized_sizes = self._standardise_sizes_check_if_legal(args_types, 
                                                                          final_sizes, 
                                                                          explicite_sizes,
                                                                          args_values_int)        
        if final_standardized_sizes == None:
            return -1
        
        resp = self._check_if_operation_allowed(keyword, args_types)
        if resp == None:
            return -1

        try:
            output = self.funtionNameLink[ keyword ](
                self.HR,
                self.FR,
                self.data,
                self.variables,
                self.labels,
                destination = destination,
                source_params = elements_in_line[1:],
                param_types = args_types,
                final_size = final_standardized_sizes,
                args_values_raw = args_values_raw,
                args_values_int = args_values_int,
                line = line
            )
        except Exception as e:
            instruction_error(self.language, self.curr_line + 1, e)
            return -1

        return output

    def load_new_state_after_change(self, change : dict, forward : bool):
        """The purpose of this method is to directly change state of the simulated
        HR, FR, DATA or manipulate date, allowing to undo/redo instruction, and
        ommit resource-intensive processing, when running already processed instructions
        """

        source = "new_value" if forward else "oryginal_value"

        for modified_elem in change:
            changes = change[modified_elem]
            match modified_elem:
                case "register":
                    for modification in changes:
                        reg = modification['location']
                        self.HR.writeIntoRegister(reg, modification[source])
                case "flags":
                    self.FR.setFlagRaw(changes[source])
                case "memory":
                    for modification in changes:
                        start = modification["location"]
                        self.data.modify_data(start, modification[source])

    def _separate_keyword(self, line : str) -> tuple[str, int]:
        """Extracts keyword from line, and returns it in capital leters. Keyword is defined as
        first non-epmty sequence of letters, which ends when space of tabulator is detected"""
        
        fs, ft = line.find(" "), line.find("\t")
        smaller, greater = min(fs, ft), max(fs, ft)
        if smaller == greater:
            not_kw_char_index = len(line)
        else:
            not_kw_char_index = smaller if smaller != -1 else greater
        
        return line[:not_kw_char_index].upper(), not_kw_char_index

    def _extract_explicite_size_def(self, arguments : list) -> tuple[list, list]:
        """This function extracts explicite sizes definitions. It returns extracted sizes,
        and arguments without explicite sizes"""

        sizes, args_no_sizes = [], []

        for arg in arguments:
            first_word = ""
            for counter, char in enumerate(arg.upper()):
                if char.isalpha():
                    first_word += char
                else:
                    break
            
            if first_word in allowed_data_types:
                sizes.append(return_size_from_name(first_word))
                args_no_sizes.append(arg[counter:].strip())
            else:
                sizes.append(None)
                args_no_sizes.append(arg)

        return sizes, args_no_sizes

    def _detect_argument_type(self, list_of_arguments : list) -> list:
        """This function parses arguments in line and detects to which category they belong:
        -   register
        -   label (technically an immediate address in memory)
        -   memory call
        -   value (or complex value if it has to be calculated on runtime)
        """
        
        types_of_args = []

        for arg in list_of_arguments:
            contain_arithm = any(filter(is_arithmetic, arg))
            contain_brack = any(filter(is_rect_bracket, arg)) 
            if contain_brack:
                types_of_args.append("memory call")
            elif contain_arithm:
                types_of_args.append("complex value")
            elif arg in self.variables:
                types_of_args.append("complex value")
            elif arg in self.labels:
                types_of_args.append('label')
            elif arg.upper() in self.HR.listRegisters():
                types_of_args.append("register")
            elif return_if_base_16_value(arg):
                types_of_args.append("value")
            elif return_if_base_10_value(arg):
                types_of_args.append("value")
            elif return_if_base_8_value(arg):
                types_of_args.append("value")
            elif return_if_base_2_value(arg):
                types_of_args.append("value")
            else:
                types_of_args.append("undefined")

        return types_of_args
    
    def _define_arg_types_and_value(self, elements : list):
        """This funciton parses list with elements detected in expression, 
        assigns types to elements, and extract values stores in elements"""

        types, values = [], []

        for e in elements:
            if e in self.variables:
                types.append("var")
                values.append(str(self.variables[e]['address']))
            elif e.upper() in self.HR.listRegisters():
                types.append("register")
                values.append(str(int(self.HR.readFromRegister(e), 2)))
            elif is_allowed_arithmetic(e):
                types.append(e)
                values.append(e)
            elif b16v := return_if_base_16_value(e):
                types.append("constant")
                values.append(b16v)
            elif b10v := return_if_base_10_value(e):
                types.append("constant")
                values.append(b10v)
            elif b8v := return_if_base_8_value(e):
                types.append("constant")
                values.append(b8v)
            elif b2v := return_if_base_2_value(e):
                types.append("constant")
                values.append(b2v)
            else:
                return

        return types, values

    def _check_standardize_mem_call(self, mem_call : str) -> str:
        """This funciton standardizes call for memory localtion, anlayzes it's syntax for
        errors and if everything is fine, then returns standardized argument"""
        
        processed = mem_call.replace("[", "+").replace("]","").replace(" ","").replace("\t","")
        if processed.startswith("+"):   processed = processed[1:]
        
        elements = []
        tmp = ""
        for c in processed:
            if c.isalnum():             tmp += c
            elif is_white_char(c):      continue
            else:
                if tmp:
                    elements.append(tmp)
                    tmp = ""
                if is_allowed_arithmetic(c):
                    elements.append(c)
        else:
            if tmp:         elements.append(tmp)

        response = self._define_arg_types_and_value(self, elements)
        if response == None:
            unrecognized_elem_mem_call(self.language)
            return
        else:
            types, values = response

        if types.count("var") > 1:
            double_memory_reference(self.language)
            return
        if types.count("register") > 2:
            multiple_register_reference(self.language)
            return

        if types.count("register") == 1:
            first_reg = elements[v1a := types.index("register")].upper()
            first_reg_type = self.HR.getRegisterType(first_reg)

            if first_reg_type == "multipurpose" and first_reg != "BX":
                first_reg_must_be_bx(self.language)
                return
            if first_reg_type == "pointer" and first_reg == "SP":
                cant_use_sp(self.language)
                return

        if types.count("register") == 2:
            first_reg = elements[v1a := types.index("register")].upper()
            second_reg = elements[types.index("register", v1a + len(first_reg))].upper()
            
            if first_reg == second_reg:
                register_called_twice(self.language)
                return
            
            first_reg_type = self.HR.getRegisterType(first_reg)
            second_reg_type = self.HR.getRegisterType(second_reg)
            
            if first_reg_type == second_reg_type:
                reg_same_type(self.language)
                return
            if first_reg_type == "multipurpose" and first_reg != "BX":
                first_reg_must_be_bx(self.language)
                return
            if (first_reg_type == "pointer" and first_reg == "SP") or \
               (second_reg_type == "pointer" and second_reg == "SP"):
                cant_use_sp(self.language)
                return
        
        standardized = "".join(values)

        return standardized

    def _check_standardize_complex_value(self, complex_value : str) -> str:
        """This function checks if the arguments which are passed are correct"""

        elements = []
        tmp = ""
        for c in complex_value:
            if c.isalnum():             tmp += c
            elif is_white_char(c):      continue
            else:
                if tmp:
                    elements.append(tmp)
                    tmp = ""
                if is_arithmetic(c):
                    if c not in ["+","-"]:  elements.append(c)
                    else:   tmp += c
                if c in ['(',')']:
                    elements.append(c)
        else:
            if tmp:         elements.append(tmp)

        """It is allowed to have values which - in general - are known at assembly
        time"""

        response = self._define_arg_types_and_value(self, elements)
        if response == None:
            unrecognized_value_compl_val(self.language)
            return
        else:
            _, values = response

        return "".join(values)

    def _check_validity_of_arguments_return_stadardized(self, arguments : list, 
            types : list) -> list:
        """This function checks if the arguments which are passed are correct"""

        validated_args = []

        for arg, atype in zip(arguments, types):
            if atype == "memory call":
                response = self._check_standardize_mem_call(arg)
                if response == None:
                    return
                validated_args.append(response)
            elif atype == "complex value":
                response = self._check_standardize_complex_value(arg)
                if response == None:
                    return
                validated_args.append(response)
            else:
                validated_args.append(arg)

        return validated_args

    def _extract_argument_value_and_size(
            self, args : list,
            args_types : list,
            sizes : list) -> tuple[list[str], list[int]]:
        """This function read arguments and gets their values. As an output it returns oryginal
        values, and values converted to int, as well as sizes"""

        source_values = []
        converted_values = []
        final_sizes = []
        destination = None

        for arg, atype, size in zip(args, args_types, sizes):
            match atype:
                case "label":
                    value = self.labels[arg]
                    source_values.append(value)
                    converted_values.append(value)
                    final_sizes.append(size if size else 16)
                case "value":
                    if sv := return_if_base_16_value(arg):
                        source_values.append(sv)
                        converted_values.append(int(sv, 16))
                    elif sv := return_if_base_10_value(arg):
                        source_values.append(sv)
                        converted_values.append(int(sv))
                    elif sv := return_if_base_8_value(arg):
                        source_values.append(sv)
                        converted_values.append(int(sv, 8))
                    elif sv := return_if_base_2_value(arg):
                        source_values.append(sv)
                        converted_values.append(int(sv, 2))
                    if size:
                        final_sizes.append(size)
                    else:
                        final_sizes.append(8 if converted_values[-1] <= 255 else 16) 
                case "complex value":
                    value = simple_eval(arg)
                    source_values.append(str(value))
                    converted_values.append(value)
                    if size:
                        final_sizes.append(size)
                    else:
                        final_sizes.append(8 if converted_values[-1] <= 255 else 16) 
                case "register":
                    value = self.HR.readFromRegister(arg.upper())
                    source_values.append(value+"b")
                    converted_values.append(int(value, 2))
                    final_sizes.append(self.HR.getSize(arg.upper()))
                case "memory call":
                    if not size:
                        size = final_sizes[0] if len(final_sizes) == 1 else 8
                    final_sizes.append(size)
                    data_in_mem = self.data.get_data(simple_eval(arg), size // 8)
                    data_in_bits = (map(lambda z: z.zfill(8), map(lambda x: x[2:], 
                                                              map(bin, data_in_mem))))
                    data_in_bits_str = "".join(data_in_bits)
                    source_values.append(data_in_bits_str + "b")
                    conv_data = int(data_in_bits_str, 2)
                    converted_values.append(conv_data)
            if len(source_values) == 1:
                destination = arg
                if atype == "memory call":
                    destination = simple_eval(arg)

        return source_values, converted_values, final_sizes, destination

    def _standardise_sizes_check_if_legal(self, arg_types : list, sizes : list, expli_sizes : list,
                                          args_values_int : list) -> list:
        """This function asks for list with detected sizes and list with detected types and
        werifies that sizes are correctly defined (should be equal)

        Posible combinations, and general ideas:

        - memory, value   -   [memory, ____ value] : explicite size diff. req. in ____
        - memory, reg     -   allowed regardless of reg value
        - memory, memory  -   ILLEGAL
        - reg, value      -   legal, but if explicite value size is passed it has to match reg size
        - reg, reg        -   illegal if right register is bigger than the left one
        - reg, memory     -   legal, no specified size required
        - value, value    -   illegal
        - value, reg      -   illegal
        - value, memory   -   illegal
        - value           -   no explicite size required
        - reg             -   no explicite size requirements
        - ___ [memory]    -   explicite size required in place of ___
        """

        if not arg_types:   return []

        match arg_types:
            case ["memory", "value"]:
                size = None
                if all(expli_sizes) and expli_sizes[0] != expli_sizes[1]:
                    explicite_sizes_mismatch(self.language)
                    return
                if expli_sizes[0]:      size = expli_sizes[0]
                elif expli_sizes[1]:    size = expli_sizes[1]
                else:
                    no_explicite_size(self.language)
                    return
                return size
                
            case ['memory', 'register']:
                mem_exp_size = expli_sizes[0]
                reg_exp_size = expli_sizes[1]
                reg_det_size = sizes[1]

                if reg_exp_size and reg_exp_size < reg_det_size:
                    explicite_size_ignored(self.language)
                
                final_reg_size = max(reg_exp_size, reg_det_size) if reg_exp_size else reg_det_size

                if mem_exp_size and mem_exp_size < final_reg_size:
                    explicite_sizes_mismatch(self.language)
                    return
                
                return final_reg_size
            
            case ['memory', 'memory']:
                cant_call_mem_twice(self.language)
                return
            
            case ["register", "value"]:
                reg_exp_size = expli_sizes[0]
                reg_det_size = sizes[0]
                var_exp_size = expli_sizes[1]
                var_det_size = sizes[1]

                if (reg_exp_size and reg_exp_size < reg_det_size) or \
                    (reg_det_size < var_det_size):
                    explicite_size_ignored(self.language)
                
                if var_exp_size and reg_det_size > var_exp_size:
                    explicite_sizes_mismatch(self.language)
                    return

                return reg_det_size
            
            case ["register", "register"]:
                return sizes[0]
            
            case ["register", "memory"]:
                reg_exp_size = expli_sizes[0]
                reg_det_size = sizes[0]
                mem_exp_size = expli_sizes[1]
                mem_det_size = sizes[1]
                
                if reg_exp_size and reg_det_size != reg_exp_size:
                    explicite_size_ignored(self.language)
                
                if mem_exp_size and reg_det_size != mem_exp_size:
                    explicite_sizes_mismatch(self.language)
                    return
                
                return reg_det_size
            
            case ['value', 'value']:
                cant_call_mem_twice(self.language)
                return
            
            case ['value', 'register']:
                cant_call_mem_twice(self.language)
                return
            
            case ['value', 'memory']:
                cant_call_mem_twice(self.language)
                return
            
            case ['memory']:

                if expli_sizes[0] == None:
                    no_explicite_size(self.language)
                    return
                
                return expli_sizes[0]

            case ['value']:
                if expli_sizes[0] != None:
                    return expli_sizes[0]
                int_value = args_values_int[0]
                if int_value < 2**8:
                    det_size = 8
                else:
                    det_size = 16
                return det_size

            case ['register']:
                reg_exp_size = expli_sizes[0]
                reg_det_size = sizes[0]

                if reg_exp_size and reg_det_size != reg_exp_size:
                    explicite_size_ignored(self.language)
                
                return reg_det_size

    def _check_if_operation_allowed(self, keyword : str, params):
        """This operation would ensure that function have the required
        amount of params passed - it assumes that each funciton defined and used
        in the program have """

        if not len(params) in self.funtionNameLink[keyword].params_range:
            wrong_no_of_params(self.language, len(params))
            return
        
        if not tuple(params) in self.funtionNameLink[keyword].allowed_params_combinations:
            wrong_combination_params(self.language, params)
            return

    def _standardize_case_for_register_names(self, elements : list, mapped_params : list):
        """This funciton ensures that all calls for register are in capital names"""

        for i in range(len(elements)):
            mp = mapped_params[i]
            if mp == "register":
                elements[i] = elements[i].upper()

        return elements

    def _prepareFunctions(self):
        """Is responsible for creating an addresable list of function since
        users usualy call funciton by names represented by string and not by
        a name of the function in program itself (which can be the same, but not for 
        the program). This would allow to match between string and a function
        and then execute the command based on the match"""

        self.funtionNameLink = {k:v for k,v in globals().items() if k.isupper()}
        self.funcSignature = {}  # Keeps the function signagure in a human-readible form
        self.funcArguments = {}  # Keeps the information about signature - necessary for the program

        # defining the function signature and default argument types needed
        for f in self.funtionNameLink:
            if type(self.funtionNameLink[f]) != dict:
                # division for arguments
                description = str(signature(self.funtionNameLink[f]))
                self.funcSignature[f] = description
                wynik = description.split(" -> ")
                zwrot = wynik[-1] if "->" in description else None
                argm = wynik[0].replace("(","").replace(")","").split(", ")
                argtyp = [
                    e.split(": ") if ":" in e else [e,"any"] for e in argm if e != ""
                    ]
                info = {}
                if argtyp == []:
                    info["arg"] = None
                else:
                    info["arg"] = {}
                    for e in argtyp:
                        if " = " in e[1]:
                            para = e[1].split(" = ")
                            info["arg"][e[0]] = {para[0] : para[1] if para[1] != "''" else ""}
                        else:
                            info["arg"][e[0]] = e[1]
                info["ret"] = zwrot
                self.funcArguments[f] = info
            else:
                self.funcArguments[f] = "dict"

        self.funcList = [name for name in self.funcSignature]    # List all functions available
