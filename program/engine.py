"""
This file contains Engine Class, which is responsible for simluation of operations on memory
"""

from inspect import signature
from .helper_functions import *
from .hardware_memory import DataSegment
from .flag_register import FlagRegister
from simpleeval import simple_eval
from .assembly_instructions import *
from .hardware_registers import HardwareRegisters
from .code_warnings import ExecutionOfOperationInLineWarning, ExpliciteSizeOperandIgnoredWarning
from .errors import (ArgumentNotExpected,
                    NoExplicitSizeError,
                    ExecutionOfOperationInLineError,
                    UnrecognizedArgumentInLineError,
                    SizesDoesntMatchError,
                    NoExpliciteSizeDefinitionWhenRequiredError,
                    KeywordNotImplementedError)

allowed_data_types = ['BYTE', 'WORD', 'DWORD', 'QWORD']

class Engine():
    """
    This class is responsible for execution of instructions within program. It has access
    to virutal hardware, and given the instruction, it executes it, and modifies the registers
    and flags accordingly
    """

    def __init__(self):
        self._prepareFunctions()
        self.HR = HardwareRegisters()
        self.FR = FlagRegister()
        self.data = DataSegment()
        self.variables = []

    def informAboutLabels(self, labels : list):
        self.labels = labels

    def informAboutVariables(self, variables : list):
        self.variables = variables

    def executeInstruction(self, line : int, command : str):
        """This function is responsible for command execution - it cuts the line, extracting command
        from arguments, defines what types are the arguments, defines what they represent, and passes
        so prepared elements to _functionExecutor()"""
        
        self.curr_line = line
        elements_in_line = []

        keyword, first_non_keyw_char = self._separate_keyword(command)
        if keyword not in self.funtionNameLink:
            raise ExecutionOfOperationInLineError(KeywordNotImplementedError())
        elements_in_line.append(keyword)
        
        arguments = command[first_non_keyw_char:].strip().split(",")
        arguments = [arg.strip() for arg in arguments if arg]
        elements_in_line.extend(arguments)

        explicite_sizes, arguments_no_size = self._extract_explicite_size_def(arguments)
        args_cleaned = list(map(lambda x: x.strip(), arguments_no_size))

        args_types = self._detect_argument_type(args_cleaned)
        if "undefined" in args_types:
            raise ExecutionOfOperationInLineError(UnrecognizedArgumentInLineError())

        args_checked = self._check_validity_of_arguments_return_stadardized(args_cleaned, args_types)

        extracted = self._extract_argument_value_and_size(args_checked, args_types, explicite_sizes)
        args_values_raw, args_values_int, final_sizes, destination = extracted
        
        for i, arg in enumerate(args_types):
            if arg == "complex value":
                args_types[i] = "value"
            elif arg == "memory call":
                args_types[i] = "memory"

        final_standardized_sizes = self._standardise_sizes_check_if_legal(args_types, 
                                                                          final_sizes, 
                                                                          explicite_sizes,
                                                                          args_values_int)

        self._check_if_operation_allowed(keyword, args_types)

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
            raise ExecutionOfOperationInLineError(exception=e)

        return output

    def load_new_state_after_change(self, change : dict, forward : bool):
        """
        The purpose of this method is to directly change state of the simulated
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
        """Extracts keyword from line, and returns it in capital leters. Keyword is defined as:
        
        - first non-epmty sequence of letters, which ends when space of tabulator is detected"""

        keyword = ""
        counter = 0
        for c in line:
            if c not in [" ", "\t"]:
                keyword += c
                counter += 1
            else:
                break
        keyword = keyword.upper()

        return keyword, counter

    def _extract_explicite_size_def(self, arguments : list) -> tuple[list, list]:
        """This function extracts explicite sizes definitions. It returns extracted sizes,
        and arguments without explicite sizes"""

        sizes = []
        args_no_sizes = []

        for arg in arguments:
            first_word = ""
            counter = 0
            for c in arg.upper():
                if c.isalpha():
                    first_word += c
                    counter += 1
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
            elif return_if_base_2_value(arg):
                types_of_args.append("value")
            else:
                types_of_args.append("undefined")

        return types_of_args

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

        types = []
        values = []
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
                raise Exception()

        if types.count("var") > 1:          raise Exception()
        if types.count("register") > 2:     raise Exception()

        if types.count("register") == 2:
            first_reg = elements[v1a := types.index("register")].upper()
            second_reg = elements[types.index("register", v1a + len(first_reg))].upper()
            
            if first_reg == second_reg: raise Exception()
            
            first_reg_type = self.HR.getRegisterType(first_reg)
            second_reg_type = self.HR.getRegisterType(second_reg)
            
            if first_reg_type == second_reg_type:
                raise Exception()
            if first_reg_type == "multipurpose" and first_reg_type != "BX":
                raise Exception()
            if (first_reg_type == "pointer" and first_reg == "SP") or \
               (second_reg_type == "pointer" and second_reg == "SP"):
                raise Exception()
        
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

        types = []
        values = []
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
                raise Exception()

        return "".join(values)

    def _check_validity_of_arguments_return_stadardized(self, arguments : list, 
            types : list) -> list:
        """This function checks if the arguments which are passed are correct"""

        validated_args = []

        for arg, atype in zip(arguments, types):
            if atype == "memory call":
                validated_args.append(self._check_standardize_mem_call(arg))
            elif atype == "complex value":
                validated_args.append(self._check_standardize_complex_value(arg))
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
                        if len(final_sizes) == 1:
                            size = final_sizes[0]
                        else:
                            size = 8
                    final_sizes.append(size)
                    data_in_mem = self.data.get_data(simple_eval(arg), size // 8)
                    data_in_bits = (map(lambda z: z.zfill(8), map(lambda x: x[2:], map(bin, data_in_mem))))
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
        werifies that sizes are correctly defined (should be equal)"""

        if not arg_types:   return []

        """
        Posible combinations, and general ideas:

        memory, value   -   [memory, ____ value] : explicite size diff. req. in ____
        memory, reg     -   allowed regardless of reg value
        memory, memory  -   ILLEGAL
        
        reg, value      -   legal, but if explicite value size is passed it has to match reg size
        reg, reg        -   illegal if right register is bigger than the left one
        reg, memory     -   legal, no speciphied size required
        
        value, value    -   illegal
        value, reg      -   illegal
        value, memory   -   illegal

        value           -   no explicite size required
        reg             -   no explicite size requirements
        ___ [memory]    -   explicite size required in place of ___
        """

        match arg_types:
            case ["memory", "value"]:
                size = None
                if all(expli_sizes) and expli_sizes[0] != expli_sizes[1]:
                    raise ExecutionOfOperationInLineError(SizesDoesntMatchError())
                if expli_sizes[0]:      size = expli_sizes[0]
                elif expli_sizes[1]:    size = expli_sizes[1]
                else:
                    raise ExecutionOfOperationInLineError(NoExplicitSizeError())
                return size
                
            case ['memory', 'register']:
                mem_exp_size = expli_sizes[0]
                reg_exp_size = expli_sizes[1]
                reg_det_size = sizes[1]

                if reg_exp_size and reg_exp_size < reg_det_size:
                    
                    raise ExecutionOfOperationInLineWarning(
                        ExpliciteSizeOperandIgnoredWarning(),
                        self.curr_line)
                
                final_reg_size = max(reg_exp_size, reg_det_size) if reg_exp_size else reg_det_size

                if mem_exp_size and mem_exp_size < final_reg_size:
                    raise ExecutionOfOperationInLineError(SizesDoesntMatchError)
                
                return final_reg_size
            
            case ['memory', 'memory']:
                raise ExecutionOfOperationInLineError()
            
            case ["register", "value"]:
                reg_exp_size = expli_sizes[0]
                reg_det_size = sizes[0]
                var_exp_size = expli_sizes[1]
                var_det_size = sizes[1]

                if reg_exp_size and reg_exp_size < reg_det_size:
                    raise ExecutionOfOperationInLineWarning(
                        ExpliciteSizeOperandIgnoredWarning(),
                        self.curr_line)
                
                if var_exp_size and reg_det_size > var_exp_size:
                    raise ExecutionOfOperationInLineError(SizesDoesntMatchError)
                
                if reg_det_size < var_det_size:
                    raise ExecutionOfOperationInLineWarning(
                        ExpliciteSizeOperandIgnoredWarning(),
                        self.curr_line)

                return reg_det_size
            
            case ["register", "register"]:
                return sizes[0]
            
            case ["register", "memory"]:
                reg_exp_size = expli_sizes[0]
                reg_det_size = sizes[0]
                mem_exp_size = expli_sizes[1]
                mem_det_size = sizes[1]
                
                if reg_exp_size and reg_det_size != reg_exp_size:
                    raise ExecutionOfOperationInLineWarning(
                        ExpliciteSizeOperandIgnoredWarning(),
                        self.curr_line)
                
                if mem_exp_size and reg_det_size != mem_exp_size:
                    raise ExecutionOfOperationInLineError(SizesDoesntMatchError)
                
                return reg_det_size
            
            case ['value', 'value']:
                raise ExecutionOfOperationInLineError()
            
            case ['value', 'register']:
                raise ExecutionOfOperationInLineError()
            
            case ['value', 'memory']:
                raise ExecutionOfOperationInLineError()
            
            case ['memory']:

                if expli_sizes[0] == None:
                    raise ExecutionOfOperationInLineError(
                        NoExpliciteSizeDefinitionWhenRequiredError())
                
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
                    raise ExecutionOfOperationInLineWarning(
                        ExpliciteSizeOperandIgnoredWarning(),
                        self.curr_line)
                
                return reg_det_size

    def _check_if_operation_allowed(self, keyword : str, params):
        """This operation would ensure that function have the required
        amount of params passed - it assumes that each funciton defined and used
        in the program have """

        if not len(params) in self.funtionNameLink[keyword].params_range:
            raise ArgumentNotExpected
        
        if not tuple(params) in self.funtionNameLink[keyword].allowed_params_combinations:
            raise ArgumentNotExpected

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
