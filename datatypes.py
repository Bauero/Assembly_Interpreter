# A single RegisterBit of a singly linked list
from array import array
import re
from helper_functions import (return_if_base_16_value,
                              return_if_base_10_value,
                              return_if_base_8_value,
                              return_if_base_2_value)
from errors import (SegmentationFault,
                    ValueIsNotANumber,
                    ModificationOutsideDataSection)

class Data:
    """
    This class is designed to keep static data which is defined in data section, but in COM app is also
    stack. As with real computer, we assume, that static data is kept within one continues line in memory - 
    therefore we can access values by asking for a range of memory - x amoung of bytes/words etc. 
    which starts at a speciphic address. By default, all valuse are assumed to take up 1 byte in
    memory. This is also assumed by 'size' property - it returns amount of bytes stored in our data.
    """

    def __init__(self):
        self.data = array('B', (0 for _ in range(2**16)))
        self.byte_counter = 0

    def add_data(self, size = 8, content = None):
        """Insert data into memory - used for .data section"""

        if content == None: return
        starting_address = self.byte_counter

        elements = []
        tmp = ''
        inside_text = False

        for char in content:
            if not inside_text and char == '"':
                inside_text = True
                tmp += char
            elif inside_text and char == '"':
                inside_text = False
                tmp += char
                elements.append(tmp)
                tmp = ''
            elif not inside_text and char == ',':
                if not tmp:
                    continue
                elements.append(tmp)
                tmp = ''
            else:
                tmp += char
        else:
            elements.append(tmp)

        for element in elements:
            is_text = False
            element = str(element).strip() if type(element) != str else element
            if element.startswith('"') and element.endswith('"'):
                element = element[1:-1]
                is_text = True

            if element == "?":
                for e in range(size):
                    self.data[self.byte_counter] = 0
                continue

            elif not is_text:
                element = element.strip()

                if value := return_if_base_16_value(element):       base = 16
                elif value := return_if_base_10_value(element):     base = 10
                elif value := return_if_base_8_value(element):      base = 8
                elif value := return_if_base_2_value(element):      base = 2

                if bool(value):
                    bite_list = bin(int(element, base))[2:].zfill(size)
                    self.byte_counter = self.modify_data(self.byte_counter, bite_list)
                    continue

            for c in element:
                bite_list =  bin(ord(c))[2:].zfill(size)
                self.byte_counter = self.modify_data(self.byte_counter, bite_list)

        return starting_address , self.byte_counter - starting_address

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

        try:
            start = starting_byte
            end = start + no_of_bytes
            return self.data[start : end]
        except IndexError:
            raise SegmentationFault

    def get_data_as_str(self, starting_byte = 0, no_of_bytes = 1):
        return "".join(str(c) for c in self.get_data(starting_byte, no_of_bytes))
