"""
This class creates an data segment object, allocating 64KB of data, and allowing for it's modification
and reading
"""

from array import array
from .errors import (SegmentationFault,
                    ValueIsNotANumber,
                    ModificationOutsideDataSection)

class DataSegment:
    """
    This class is designed to keep static data which is defined in data section, but in COM app is also
    stack. As with real computer, we assume, that static data is kept within one continues line in memory - 
    therefore we can access values by asking for a range of memory - x amoung of bytes/words etc. 
    which starts at a specific address. By default, all valuse are assumed to take up 1 byte in
    memory. This is also assumed by 'size' property - it returns amount of bytes stored in our data.
    """

    def __init__(self):
        self.data = array('B', (0 for _ in range(2**16)))
        self.byte_counter = 0

    def modify_data(self, starting_byte = 0, list_of_new_bits : list[str] = []) -> int:
        """Modify in place X amount of bytes. Function returns value of counter
        
        :param: `starting_byte` - no. of starting byte which marks begining of writing
        :param: `list_of_new_bits` - list of bits forming X amount of bytes which will
        be written into memory
        """

        for byte in range(0, len(list_of_new_bits) // 8,):
            try:
                v = int("".join(list_of_new_bits[ 8*(byte) : 8 * (byte + 1) ]), 2)
                self.data[starting_byte] = v
                starting_byte += 1
            except IndexError:  raise ModificationOutsideDataSection
            except ValueError:
                raise ValueIsNotANumber(f"Value '{byte}' cannot be converted to 1's and 0's")
            
        return starting_byte

    def get_data(self, starting_byte = 0, no_of_bytes = 1):
        """Returns data in form of list with numbers representin values of successive bytes"""
        
        try:
            start = starting_byte
            end = start + no_of_bytes
            return self.data[start : end]
        except IndexError:
            raise SegmentationFault

    def get_data_raw_binary(self, starting_byte = 0, no_of_bytes = 1):
        """Returns data in form of string with 1's or 0's - represents raw binary data"""
        
        return "".join(bin(c)[2:] for c in self.get_data(starting_byte, no_of_bytes))
