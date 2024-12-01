"""
This file contains Engine Class, which is responsible for simluation of operations on memory
"""

from inspect import signature
from helper_functions import *
from stack import Stack
from flag_register import FlagRegister
from assembly_instructions.arithmetic import *
from hardware_registers import HardwareRegisters
from errors import ArgumentNotExpected, NoExplicitSizeError, ExecutionOfOperationInLineError


################################################################################
#   Constants
################################################################################


allowed_data_types = ['BYTE', 'DB', 'WORD', 'DW', 'DWORD', 'DD', 'QWORD', 'DQ']


################################################################################
#   Main Class
################################################################################


class Engine():
    """
    This class is responsible for execution of instructions within program. It has access
    to virutal hardware, and given the instruction, it executes it, and modifies the registers
    and flags accordingly
    """

    ############################################################################
    #   Public Methods
    ############################################################################

    def __init__(self):
        self._prepareFunctions()
        self.HR = HardwareRegisters()
        self.FR = FlagRegister()
        self.ST = Stack()

    def informAboutLabels(self, labels : list):
        self.labels = labels

    def informAboutVariables(self, variables : list, data : Data):
        self.variables = variables
        self.data = data

    def executeCommand(self, command : str):
        """This function is responsible for command execution - it splits line to under"""

        elements_in_line = []

        # cut spaces
        no_spaces = filter(lambda x: bool(x), command.split(" "))
        
        for element in no_spaces:
            # cut every 'space-separated' peace if it contains ','
            elements_in_line.extend(filter(lambda x: bool(x),element.split(',')))

        # Explicitly ignore elements of command

        def _to_ignore(element : str):
            return element.lower() in ['ptr']

        elements_in_line = [filter(_to_ignore, elements_in_line)]

        # Fix for case when explicite value length is given
        #   ['mov', 'word', '[bp]', '32'] -> ['mov', 'word [bp]', '32']
        tmp = []
        stc = ''
        for i in range(0, len(elements_in_line)):
            if elements_in_line[i].upper() in allowed_data_types:
               stc = elements_in_line[i]
            else:
                if stc:
                    tmp.append(f"{stc} {elements_in_line[i]}")
                    stc  = ''
                else:
                    tmp.append(elements_in_line[i])
        elements_in_line = tmp
             
        #   ['mov', 'AX', '10'] -> ['keyword', 'register', 'value']
        elements_types = list(map(lambda e: self._define_element_type(e), elements_in_line))
        
        
        assert elements_in_line, f"Line '{command}' seems to contain no values to process"
        assert elements_types[0] == 'keyword', \
                f"First element in line '{command}' is of type {elements_types[0]} - only"+ \
                    " values type 'keyword' are allowed"
        mapped_params = self._check_if_operation_allowed(elements_in_line[0], elements_in_line[1:])

        #   ['mov', 'AX', '10'] -> [329, 10] or  ['add', 'var1', 'word 20'] -> [70, 20]
        values = list(map(lambda e: self._get_value_or_address(
                            elements_in_line[1:],
                            mapped_params
                        ), elements_in_line))
        
        output = self._functionExecutor(
            elements_in_line[0], 
            source_params = elements_in_line[1:],
            param_types = elements_types[1:],
            values = values
            )

        if output:
            #   TODO Add support to stuff like output to terminal
            ...

    ############################################################################
    #   Private Methods
    ############################################################################

    def _functionExecutor(self, function : str, **kwargs):
        """
        Is called on every line of code - it's job is to execute order from above
        on the memory of our program

        This function links apropriate function with input
        
                                functionExecutor 
        
        Arguments       ----------------------->    Apriopriate function in the program
        
        EX:

        function: 'ADD' | arg1: 'AX' | arg2: 'BX' -----> ADD(r = 'AX', s = 'BX')
        """

        if function in self.funtionNameLink:
            try:
                output = self.funtionNameLink[function](
                    self.HR, self.FR, self.ST, self.data, kwargs
                )
                return output
            except Exception as e:
                raise ExecutionOfOperationInLineError(e)
        else:
            raise NotImplementedError
        
    def _define_element_type(self, element : str):
        """Define in which catergory an element belongs - also checks if it's valid:
        
        - keyword           (mov)
        - variable          (tmp1)
        - [variable]        ([tmp1])
        - register          (AX)
        - [address_in_reg]  ([BX])
        - ***TODO*** procedure  (like MyProcedure PROC)
        - [address_value]   ([20h])
        - [combo_address]   ([BX+20h])
        - value             (word 10h, or 20 or 10b)
        - undefined         (anything else, which doesn't match the filters)
        """

        def _call_eff_add_in_reg(element : str):
            """Is it call for effective address stored in register?"""
            return element.startswith("[") and element.endswith("]") and \
                    element[1:-1].upper() in self.HR.listRegisters()

        def _call_for_var_content(element : str):
            """Is it call to get content stored under address defined by variable ?"""
            
            final_element = element
            
            if " " in element:
                if element.split(" ")[0].upper() in allowed_data_types:
                    final_element = element.split(" ")[-1]
                else:
                    return False
            
            return final_element.startswith("[") and \
                     final_element.endswith("]") and \
                        final_element in list(self.variables)
        
        def _is_call_for_value_under_address(element : str):
            """Return True if value is call to access memory stored under some address"""
            if not (element.startswith("[") and element.endswith("]")): return False
            if not "+" in element:  return False

            return True

        def _check_if_value_is_number(element : str):

            to_check_for_being_number = element

            if " " in element:
                if element.split(" ")[0].upper() in allowed_data_types:
                    to_check_for_being_number = element.split(" ")[-1]
                else:
                    return False
            
            if return_if_base_2_value(to_check_for_being_number):
                return True
            elif return_if_base_10_value(to_check_for_being_number):
                return True
            elif return_if_base_16_value(to_check_for_being_number):
                return True
            
            return False    
        
            
        if element.upper() in self.funcList:
            return "keyword"
        elif element.upper() in self.HR.listRegisters():
            return "register"
        elif _call_eff_add_in_reg(element):
            return "[address_in_reg]"
        elif element in list(self.variables):
            return "variable"
        elif _call_for_var_content(element):
            return "[variable]"
        #   TODO
        # elif element in list(self.procedures):
        #     return "procedure"
        elif _is_call_for_value_under_address(element):
            return "[combo_address]"
        elif _check_if_value_is_number(element):
            return "value"
        else:
            return "undefined"

    def _check_if_operation_allowed(self, keyword : str, *params):
        """This operation would ensure that function have the required
        amount of params passed - it assumes that each funciton defined and used
        in the program have """

        if not len(params) in self.funtionNameLink[keyword].params_range:
            return False
        
        """ 
        Allowed combinations, and it's numbers
            1. variable          (tmp1)
            2. [variable]        ([tmp1])
            3. register          (AX)
            4. [address_in_reg]  ([BX])
            5. [address_value]   (word [20h])
            6. [combo_address]   ([BX+20h])
            7. value             (word 10h, or 20 or 10b)"""
        
        def _map_values(value : str) -> int:
            match value:
                case "variable":            return 1
                case "[variable]":          return 2
                case "register":            return 3
                case "[address_in_reg]":    return 4
                case "[address_value]":     return 5
                case "[combo_address]":     return 6
                case "value":               return 7
            return -1
        
        mapped_params = tuple(map(_map_values, params))
        
        if not mapped_params in self.funtionNameLink[keyword].allowed_params_combinations:
            raise ArgumentNotExpected
        else:
            return mapped_params

    def _get_value_or_address(self, elements : list, mapped_params : tuple):
        """
        This function is responsible for getting either address of value of the param
        """
        values = []

        for id, elem_type in enumerate(mapped_params):
            
            match elem_type:
                case 1:
                    values.append(self.variables[elements[id]]['address'])
                case 2:
                    values.append(self.variables[elements[id][1:-1]]['value'])
                case 3:
                    values.append(self.HR.readFromRegister(elements[id]))
                case 4:
                    try:
                        size, register = elements[id].split(' ')
                        if size.upper() not in allowed_data_types:
                            raise ValueError
                    except ValueError:
                        raise NoExplicitSizeError(f"No explicite size definition in '{elements[id]}'")

                    starting_point = self.HR.readFromRegister(register[1:-1])
                    starting_point = int(starting_point, base=2)

                    size = return_size_from_name(size)

                    values.append(self.data.get_data_as_str(starting_point, size = size))
                case 5:
                    try:
                        size, register = elements[id].split(' ')
                        if size.upper() not in allowed_data_types:
                            raise ValueError
                    except ValueError:
                        raise NoExplicitSizeError(f"No explicite size definition in '{elements[id]}'")

                    address = convert_number_to_int_with_binary_capacity(register[1:-1], 16)
                    size = return_size_from_name(size)
                    values.append(self.data.get_data_as_str(address, size = size))
                case 6:
                    #TODO
                    values.append(None)
                case 7:
                    try:
                        size = 16
                        if ' ' in elements[id].strip():
                            size, number = elements[id].split(' ')
                            if size.upper() not in allowed_data_types:
                                raise ValueError
                        values.append(convert_number_to_bits_in_str(number, size))
                    except ValueError:
                        raise NoExplicitSizeError(f"No explicite size definition in '{elements[id]}'")

        return values

    def _get_argument(self, argument : str):
        """This function is responsible for extraction of data, so that keywords
        can outsorce exctraction of values stored withn passed arguments"""


        """
        Mój problem polega na tym, że mamy dwie metody na rozpisanie tego jak zostają
        zmienione rejesty i hardware w momencie kiedy jest uruchamiana funkcja - pytanie
        pojawia się, kiedy chcemy dokonać oceny tego czy dana operacja jest dozwolona, lub jak zapisać argumenty:
        
        - gdzie powinna następować decyzja o tym, czy dany zestaw parametrów jest dopuszczalny
        - gdzie powinien następować odczyt
        - jak nadpisywać / odczytywać rejestry, zmienne i stos i dane

        Przypadek 1 - dzieje się to po stronie silnik
        
        Zalety:
        + uproszczony kod - odczyty i zapisy realizujemy po stronie silnika, unikając redundancji
        w przygotowaniu
        + jesteśmy w stenie uprościć kod funkcji

        Wady:
        - musimy być gotowi na różne wymagania funkcji - z tego powodu będziemy musieli mieć
        wiedzę, nt. wymagań i sygnatury funkcji "na wstępie"
        """

    #   Methods executed only at ititialization

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

        self.funcList = [self.funcSignature]    # List all functions available
