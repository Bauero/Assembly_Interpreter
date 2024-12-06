"""
This file is responsible for managing opened file - loading it, and then passin instruction
to engine. It can communicate with engine to provide functionali like calling functions,
or jumps. It is also responible for managing history or operations done by program
"""

from preprocessor import loadMainFile
from helper_functions import loadFileFromPath

class CodeHandler():
    """
    This class is responsible for handlind opened files - it passes lines for execution, 
    handles opened file and loades instruction for engine
    """

    def __init__(self, engine):
        self.openFiles = []
        self.fileExecLine = {}
        self.rawfiles = {}
        self.files = {}
        self.currentlyExecutedFile = ""
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
        self.start = start
        self.currentlyExecutedFile = path_to_file
        self.openFiles.append(path_to_file)
        self.files[path_to_file] = preprocessed_instrucitons

        if start != (-1, [-1]):
            return start[1]

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
        self.engine.executeCommand(command)

    def gcefat(self):
        """Get Currently Executed File As Text"""
        return  "".join(self.rawfiles[self.currentlyExecutedFile])
    
    def set_interactive_mode(self, value : bool):
        self.working_in_interactive_mode = value
