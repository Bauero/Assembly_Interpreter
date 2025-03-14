"""
This module is responsible for handling and storing instructions, as well as permanent
storage of state of the program if one want's to save the current state as a file, for
later
"""

from .hardware_memory import DataSegment as Ds
from .hardware_registers import HardwareRegisters as Hr
from .flag_register import FlagRegister as Fr

class History():
    """
    History class creates and object which stores information about current progress of
    program running, which allows for clean access from the main program
    """

    def __init__(self, path_to_file, raw_file, preprocessed_instructions):
        self._path_to_file = path_to_file
        self._raw_file = raw_file
        self._preprocessed_instructions = preprocessed_instructions
        self._history = []
        self._current_instruction = -1

    def load_next_instruction_if_executed(self) -> tuple[int, dict] | None:
        """Load new instruction if it's not already done"""
        
        if self._current_instruction + 1 == len(self._history):
            return None
        self._current_instruction += 1
        record = self._history[self._current_instruction].values()
        _, change, next_line = record
        return next_line, change

    def load_previous_instruction_if_executed(self) -> tuple[int, dict] | None:
        """Load previous instruction if there are any done before the current"""
        
        if self._current_instruction == -1:
            return None
        record = self._history[self._current_instruction].values()
        exec_line, change, _ = record
        self._current_instruction -= 1
        return exec_line, change

    def add_new_instruction(self, executed_line : str, change : str, next_line : str):
        """Enters new successful instruction into history"""
        
        entry = {
            "executed_line" : executed_line,
            "change" : change,
            "next_line" : next_line,
        }
        self._history.append(entry)
        self._current_instruction += 1

    def history_length(self):
        """Return number of all entries"""
        return len(self._history)
    
    def save_final_state(self, HR : Hr, FR : Fr, data : Ds, variables : list):
        """
        This instruction allows for saving state of additional elements, for
        storage. By default those elements are not saved, as the values are kept
        in engine as classes at runtime
        """
        
        self.HR = HR
        self.FR = FR
        self.data = data
        self.variables = variables

    def return_saved_state(self) -> tuple[Hr, Fr, Ds, list, str, str, list]:
        """
        This instruction returns all values kept for storage in history file,
        and then deletes all values which don't have to be stored constantly in
        history file
        """

        return_all =  (self.HR, self.FR, self.data, self.variables,
                        self._path_to_file, self._raw_file, 
                        self._preprocessed_instructions)

        del self.HR
        del self.FR
        del self.data
        del self.variables

        return return_all
