"""
This file is responsible for managing opened file - loading it, and then passin instruction
to engine. It can communicate with engine to provide functionali like calling functions,
or jumps. It is also responible for managing history or operations done by program
"""

from .preprocessor import loadMainFile
from .helper_functions import loadFileFromPath
from .history import History
from .engine import Engine
import pickle

class CodeHandler():
    """
    This class is responsible for handlind opened files - it passes lines for execution, 
    handles opened file and loades instruction for engine
    """

    def __init__(self, engine : Engine):
        self.openFiles = []
        self.rawfiles = {}
        self.files = {}
        self.currentlyExecutedFile = ""
        self.currentlyExecutedLine = {}
        self.engine = engine
        self.working_in_interactive_mode = False

    def readPrepareFile(self, path_to_file : str, ignore_size_limit : bool, 
                        ignore_file_type : bool) -> list[int]:
        """This function, reads file and prepare it's content for processing"""

        raw_file = loadFileFromPath(path_to_file, ignore_size_limit, ignore_file_type)

        self.rawfiles[path_to_file] = raw_file                                              # Zapisanie ścieżki dostępu do pliku
        start, preprocessed_instrucitons = loadMainFile(raw_file, self.engine.DS)         # Wstępna analiza z użyciem preprocesor.py
        self.pass_variable_to_engine(preprocessed_instrucitons)                             # Przekazanie listy zmiennych do silinika

        self.currentlyExecutedFile = path_to_file                                           # Zapisanie jaki obecnie wykonywany jest plik (umożliwienie dodania wsparcia do wielu plików)
        self.currentlyExecutedLine[path_to_file] = start                                    # Zapisanie jaka linijka w jakim pliku jest wykonywana (umożliwienie dodania wsparcia do wielu plików)
        self.openFiles.append(path_to_file)                                                 # Zapisanie pełnej ścieżii do pliku w liści plików na których pracujemy
        self.files[path_to_file] = preprocessed_instrucitons                                # Zapisanie przygotowanych instrkucji wśród plików
        
        # Inicjalizacja modułu do zapisywania historii
        self.history = History(
            path_to_file,
            raw_file,
            preprocessed_instrucitons
        )

        # W przypadku pustego pliku zwrócenie wartości 0 - lista oznacza które linie program ma podkreślić - możliwość pracy na instrukcjach wielolinijkow
        output = start[1] if start != (-1, [-1]) else [0]
        
        return output

    def readInteractive(self, data : str) -> list[int]:
        """This funciton """

        text_in_linex = data.split("\n")
        
        #   Prepare data
        start, preprocessed_instrucitons = loadMainFile(text_in_linex)
        self.pass_variable_to_engine(preprocessed_instrucitons)

        #   Save variables inside Code Handler
        self.start = start
        self.files["interactive"] = preprocessed_instrucitons
        self.currentlyExecutedFile = "interactive"

        if start != (-1, [-1]): return start[1]
        
    def pass_variable_to_engine(self, preprocessed_instrucitons):
        assert type(preprocessed_instrucitons) == dict
        self.engine.informAboutLabels(preprocessed_instrucitons['labels'])
        self.engine.informAboutVariables(
            preprocessed_instrucitons['variables'],
        )

    def executeCommand(self, command, **kwargs):
        """
        This function is like transition layer between Engine and Gui - from Gui, user
        orders line exeuction, code handler passes appriopriate line to engine, and controls
        that the excution was correct. This function is responsible for catching any errors
        and passing appriopriate info to Gui, which would then handle notifying user about
        what went wrong
        """

        match command:
            case 'next_instruction':        return self._run_next_instruction(**kwargs)
            case 'previous_instruction':    return self._run_previous_instruction(**kwargs)
            case 'save_history_into_file':  return self._save_history_into_file(**kwargs)
            case 'load_history_from_file':  return self._load_history_from_file(**kwargs)

    def gcefat(self):
        """Get Currently Executed File As Text"""
        return  "".join(self.rawfiles[self.currentlyExecutedFile])
    
    def set_interactive_mode(self, value : bool):
        self.working_in_interactive_mode = value

    def get_curr_exec_line(self):
        file = self.currentlyExecutedFile
        return self.currentlyExecutedLine[file]

    def _get_current_line_instr(self):
        curr_line = self.currentlyExecutedLine[self.currentlyExecutedFile][0]
        curr_inst = self.files[self.currentlyExecutedFile]['lines'][
                curr_line
        ]
        return curr_line, curr_inst

    def _run_next_instruction(self, **kwargs):
        """
        This keyword executed next instruction in our file. If we are working in history,
        and press 'next instruction' button, state after the instruction is executed,
        will be loaded from history - otherwise, instruction will be executed by engine.
        """
        
        already_executed = self.history.load_next_instruction_if_executed()

        if already_executed:
            next_line, change = already_executed
            self.engine.load_new_state_after_change(change, forward = True)
            self.engine.HR.writeIntoRegister("IP", next_line)
            lines_in_source_file = self.files[self.currentlyExecutedFile]['lines'][next_line]['lines']
            self.currentlyExecutedLine[self.currentlyExecutedFile] = \
                [next_line, lines_in_source_file]
            
            return {"status" : 0, "highlight" : lines_in_source_file}

        else:
            curr_line, curr_inst = self._get_current_line_instr()
            line_content = curr_inst['content']
            output = self.engine.executeInstruction(curr_line, line_content)
            
            if output.get("error", None):
                output["status"] = 1
                return output
            if output.get("warnings", None):
                output["status"] = 2
            
            if output == None or not "next_instruction" in output:
                if curr_line + 1 < len(self.files[self.currentlyExecutedFile]['lines']):
                    next_line = curr_line + 1
                else:
                    if output.get("status", None):
                        output["status"] = -12
                        return output
                    else:
                        return {"status" : -12}
            elif "next_instruction" in output:
                next_line = output["next_instruction"]

            self.history.add_new_instruction(curr_line, output, next_line)
            self.engine.HR.writeIntoRegister("IP", next_line)
            
            lines_in_source_file = self.files[self.currentlyExecutedFile]['lines'][next_line]['lines']
            self.currentlyExecutedLine[self.currentlyExecutedFile] = [next_line, lines_in_source_file]
        
            status = {"status" : 0, "highlight" : lines_in_source_file}
            
            return status

    def _run_previous_instruction(self, **kwargs):
        """
        Handles action when user presses "previous instruciton" button. Regarding on the
        state, it load state when previous instruction was about to be executed, if, 
        of course, we have any previous instruciton stored in history
        """

        try:
            previous_instruction = self.history.load_previous_instruction_if_executed()
            #   Load results of previous instruction from memory
            if previous_instruction:
                previous_line, change = previous_instruction
                self.engine.load_new_state_after_change(change, forward = False)
                self.engine.HR.writeIntoRegister("IP", previous_line)
                lines_in_source_file = self.files[self.currentlyExecutedFile]['lines'][previous_line]['lines']
                self.currentlyExecutedLine[self.currentlyExecutedFile] = [previous_line, lines_in_source_file]
                status = {"status" : 0, "highlight" : lines_in_source_file}

            #   Notify user, that there aren't any previous instructions
            else:
                status = {
                    "status" : 0, 
                    "highlight" : self.currentlyExecutedLine[self.currentlyExecutedFile][1]
                }
        except Exception as e:
            status = {"status" : -1, "exception" : e}
        finally:
            return status

    def _save_history_into_file(self, **kwargs):
        try:
            path = kwargs['path']

            HR  = self.engine.HR
            FR  = self.engine.FR
            DS  = self.engine.DS
            VAR = self.engine.variables

            self.history.save_final_state(HR, FR, DS, VAR)
            pickle.dump(self.history, path)

            status = {"status" : 0}
        
        except Exception as e:
            status = {"status" : -1, "exception" : e}

        finally:
            return status
        
    def _load_history_from_file(self, **kwargs):
        try:
            path = kwargs['path']

            self.history = pickle.load(path)
            output = self.history.return_saved_state()

            HR, FR, DS, VAR, path_to_file, raw_file, \
                preprocessed_instructions = output

            self.pass_variable_to_engine(preprocessed_instructions)
            self.rawfiles[path_to_file] = raw_file
            self.currentlyExecutedFile = path_to_file

            current_line = self.history.history_length()
            current_line_in_file = preprocessed_instructions['lines'][current_line]['lines']

            self.currentlyExecutedLine[path_to_file] = (current_line, current_line_in_file)
            self.openFiles.append(path_to_file)
            self.files[path_to_file] = preprocessed_instructions

            status = {"status" : 0}

        except Exception as e:
            status = {"status" : -1, "exception" : e}

        finally:
            return status
