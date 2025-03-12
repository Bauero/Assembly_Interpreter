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
        output = self.preprocessFile(path_to_file, raw_file)
        
        self.history = History(
            path_to_file,
            raw_file,
            self.files[path_to_file]
        )

        return output

    def load_file_interactive(self, file_path : str) -> list[int]:
        """This funciton """

        raw_file = loadFileFromPath(file_path, True, True)
        
        self.rawfiles["interactive"] = raw_file
        start = -1
        preprocessed_instrucitons = []

        self.currentlyExecutedFile = "interactive"
        self.currentlyExecutedLine["interactive"] = start
        self.openFiles.append("interactive")
        self.files["interactive"] = preprocessed_instrucitons
        
        self.history = History(
            "interactive",
            raw_file,
            preprocessed_instrucitons
        )
        
        return start, raw_file

    def preprocessFile(self, path_to_file : str, raw_file : list):
        self.rawfiles[path_to_file] = raw_file
        start, preprocessed_instrucitons = loadMainFile(raw_file, self.engine.DS)
        self.pass_variable_to_engine(preprocessed_instrucitons)

        self.currentlyExecutedFile = path_to_file
        self.currentlyExecutedLine[path_to_file] = start
        self.openFiles.append(path_to_file)
        self.files[path_to_file] = preprocessed_instrucitons

        output = start[1] if start != (-1, [-1]) else [0]

        return output

    def startInteractive(self, code : str):
        """This function is run, when program is activated. It checks if the 
        code is valid, are there any changes, and returns None or list with new
        lines for highlight"""

        code_lines = [line + "\n" for line in code.split("\n")]
        previous_lines = self.rawfiles.get("interactive")

        if not previous_lines or code_lines != previous_lines:

            start = self.preprocessFile("interactive", code_lines)
            self.history = History(
                "interactive",
                code_lines,
                self.files["interactive"]
            )

            return start

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
            if next_line == None:
                return {"status" : -1, "highlight" : []}
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
            
            if "next_instruction" in output:
                next_line = output["next_instruction"]
            else:
                if curr_line + 1 < len(self.files[self.currentlyExecutedFile]['lines']):
                    next_line = curr_line + 1
                    output["status"] = 0 if not output.get("warnings") else 2
                else:
                    next_line = -1
                    exec_with_warnings = bool(output.get("warnings"))
                    if exec_with_warnings:
                        self.currentlyExecutedLine[self.currentlyExecutedFile] = -1
                        output["status"] = -12
                    else:
                        output["status"] = -1

            if next_line != -1:
                self.history.add_new_instruction(curr_line, output, next_line)
                self.engine.HR.writeIntoRegister("IP", next_line)
                lines_in_source_file = self.files[self.currentlyExecutedFile]['lines'][next_line]['lines']
                self.currentlyExecutedLine[self.currentlyExecutedFile] = [next_line, lines_in_source_file]
                output["highlight"] = lines_in_source_file
            else:
                self.history.add_new_instruction(curr_line, output, None)
                self.engine.HR.writeIntoRegister("IP", 0)
                self.currentlyExecutedLine[self.currentlyExecutedFile] = [None, None]
                output["highlight"] = []
            
            return output

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

            self.engine.HR = HR
            self.engine.FR = FR
            self.engine.DS = DS
            self.engine.variables = VAR
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
