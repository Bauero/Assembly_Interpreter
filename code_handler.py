"""
This file is responsible for managing opened file - loading it, and then passin instruction
to engine. It can communicate with engine to provide functionali like calling functions,
or jumps. It is also responible for managing history or operations done by program
"""

from preprocessor import loadMainFile
from helper_functions import loadFileFromPath
from errors import ExecutionOfOperationInLineError, DetailedException

class CodeHandler():
    """
    This class is responsible for handlind opened files - it passes lines for execution, 
    handles opened file and loades instruction for engine
    """

    def __init__(self, engine):
        self.openFiles = []
        self.rawfiles = {}
        self.files = {}
        self.currentlyExecutedFile = ""
        self.currentlyExecutedLine = {}
        self.engine = engine
        self.working_in_interactive_mode = False

    def readPrepareFile(self, path_to_file, ignore_size_limit, ignore_file_type):
        """This function, reads file and prepare it's content for processing"""

        raw_file = loadFileFromPath(path_to_file, ignore_size_limit, ignore_file_type)
        
        #   Prepare data
        assert type(raw_file) == list
        self.rawfiles[path_to_file] = raw_file
        start, preprocessed_instrucitons = loadMainFile(raw_file)
        self.pass_variable_to_engine(preprocessed_instrucitons)

        #   Save variables inside Code Handler
        self.currentlyExecutedFile = path_to_file
        self.currentlyExecutedLine[self.currentlyExecutedFile] = start
        self.openFiles.append(path_to_file)
        self.files[path_to_file] = preprocessed_instrucitons

        if start != (-1, [-1]):
                return start[1]
        
        # TODO what whould happen if there is no starting poing?

    def readInteractive(self, data : str):
        text_in_linex = data.split("\n")
        
        #   Prepare data
        start, preprocessed_instrucitons = loadMainFile(text_in_linex)
        self.pass_variable_to_engine(preprocessed_instrucitons)

        #   Save variables inside Code Handler
        self.start = start
        self.files["interactive"] = preprocessed_instrucitons
        self.currentlyExecutedFile = "interactive"

        if start != (-1, [-1]):
            return start[1]
        
    def pass_variable_to_engine(self, preprocessed_instrucitons):
        assert type(preprocessed_instrucitons) == dict
        self.engine.informAboutLabels(preprocessed_instrucitons['labels'])
        self.engine.informAboutVariables(
            preprocessed_instrucitons['variables'],
            preprocessed_instrucitons['data']
        )

    def executeCommand(self, command):
        """
        This function is like transition layer between Engine and Gui - from Gui, user
        orders line exeuction, code handler passes appriopriate line to engine, and controls
        that the excution was correct. This function is responsible for catching any errors
        and passing appriopriate info to Gui, which would then handle notifying user about
        what went wrong
        """

        try:
            match command:
                case 'execute_instruction':
                    #   Check which line in which file should be executed, and pass it to engine
                    curr_line = self.currentlyExecutedLine[self.currentlyExecutedFile][0]
                    curr_inst = self.files[self.currentlyExecutedFile]['lines'][
                            curr_line
                        ]
                    #   Execute command and handle any What To Do things
                    line_content = curr_inst['content']
                    wtd = self.engine.executeInstruction(line_content)
                    
                    next_line = curr_line + 1
                    self.engine.HR.writeIntoRegister("IP", next_line)
                    lines_in_source_file = self.files[self.currentlyExecutedFile]['lines'][next_line]['lines']
                    
                    self.currentlyExecutedLine[self.currentlyExecutedFile] = \
                        [next_line, lines_in_source_file]
                    
                    status = {"status" : 0, "highlight" : lines_in_source_file}

        except ExecutionOfOperationInLineError as exc:
            org_exc = exc.source_exception()
            status = {
                "status" : 1,
                "action" : "stop",
                "exception" : org_exc 
            }
            if  org_exc.isinstance(DetailedException):
                status['line'] = org_exc.line() if org_exc.line() else curr_line
                status['message'] = org_exc.message()
        
        except NotImplementedError as e:
            status = {
                'status' : 1,
                "action" : "stop",
                "exception" : e,
                "message" : "Instruction unrecognized"
            }

        except Exception as e:
            """Handle undefined exceptions"""
            
            status = {
                "status" : -1,
                "exception" : ""
            }
        
        finally:
            return status

    def gcefat(self):
        """Get Currently Executed File As Text"""
        return  "".join(self.rawfiles[self.currentlyExecutedFile])
    
    def set_interactive_mode(self, value : bool):
        self.working_in_interactive_mode = value

    def _handle_wtd(self, wtd):
        """
        This function should be able o handle engine output, and based on that decide
        which line should be next, to execute
        """
        ...
