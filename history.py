"""
This module is responible for handling and storing instructions, as well as permanent
storage of state of the program if one want's to save the current state as a file, for
later
"""

class History():
    """
    History class creates and object which stores information about current progress of
    programm running, which allows for clean acces from the main program
    """

    def __init__(self, path_to_file, raw_file, preprocessed_instructions):
        self.path_to_file = path_to_file
        self.raw_file = raw_file
        self.preprocessed_instructions = preprocessed_instructions
        self.history = []
        self.current_instruction = -1

    def load_next_instruction_if_executed(self):
        """Load new instruction if it's not already done"""
        
        if self.current_instruction + 1 == len(self.history):
            return None

        self.current_instruction += 1
        record = self.history[self.current_instruction].values()
        exec_line, change, next_line = record
        return next_line, change

    def load_previous_instruction_if_executed(self):
        """Load previous instruction if there are any done before the current"""
        
        #   We tried to load last executed instruction - we are at the end of history
        if self.current_instruction == -1:
            return None
        record = self.history[self.current_instruction].values()
        exec_line, change, next_line = record
        self.current_instruction -= 1
        return exec_line, change

    def add_new_instruction(self, executed_line, change, next_line):
        
        entry = {
            "executed_line" : executed_line,
            "change" : change,
            "next_line" : next_line,
        }
        self.history.append(entry)
        self.current_instruction += 1

    def history_length(self):
        return len(self.history)
    
    def save_final_state(self, HR, FR, ST, data, variables):
        """
        This instruction allows for saving state of additional elements, for
        storage. By default those elements are not saved, as the values are kept
        in engine as classes at runtime
        """
        
        self.HR = HR
        self.FR = FR
        self.ST  = ST
        self.data = data
        self.variables = variables

    def return_saved_state(self):
        """
        This instruction returns all values kept for storage in history file,
        and then deletes all values which don't have to be stored constantly in
        history file
        """

        return_all =  (self.HR, self.FR, self.ST, self.data, self.variables,
                        self.path_to_file, self.raw_file, self.preprocessed_instructions)

        del self.HR
        del self.FR
        del self.ST
        del self.data
        del self.variables

        return return_all

    def print_state(self, text):
        print(text, self.current_instruction, self.history)
