# A single node of a singly linked list
import re
from errors import SegmentationFault, ValueIsNotANumber, ModificationOutsideDataSection

class Node:
    
    def __init__(self, data = 0): 
        self.data = data

    def printInt(self) -> int:
        return int(self.data)
    
    def printStr(self) -> str:
        return str(self.data)
    
class Variable:

    __variables = 0

    def __init__(self, size,  data, name):
        self.data = data
        self.name = name
        self.size = size
        self.address = self.__variables

        #   new variable has the number one grater than the previous one
        Variable.__variables += 1

    def getSize(self):
        if self.size == "dw": return 16
        elif self.size == "byte": return 8

class Data:
    """
    This class is designed to keep static data which is defined in data section. As with 
    real computer, we assume, that static data is kept within one continues line in memory - 
    therefore we can access values by asking for a range of memory - x amoung of bytes/words etc. 
    which starts at a speciphic address. By default, all valuse are assumed to take up 1 byte in
    memory. This is also assumed by 'size' property - it returns amount of bytes stored in our data.
    """

    def __init__(self):
        self.data : list = []

    @property
    def size(self):
        return len(self.data) // 8

    def add_data(self, size = 8, content = None):

        if content == None: return
        starting_address = self.size

        #   Cut string whenever , occurs - ignore instances inside text
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

            #   Skip if this is just undefiend
            if element == "?":
                for e in range(size):
                    self.data.append(0)
                continue

            is_number = False

            if not is_text:
                element = element.strip()

                #   Check if this is some kind of hexadecimal number
                if re.search(r"\b(0[xX][0-9a-fA-F]+|[0-9a-fA-F]+h)\b", element):
                    if element.endswith('h'):
                        element = "0x" + element[:-1] # "ADh" -> 0xAD
                    base = 16
                    is_number = True
                
                #   Check if this is normal number (ex. 18)
                elif re.search(r"\b(0|[1-9][0-9]*)\b", element):
                    base = 10
                    is_number = True

                elif re.search(r"\b[01]+[bB]\b", element):
                    is_number = False
                    # cut the 'b' at the end, and the number is ready for save
                    element = element[:-1]
            
            if is_number:
                converted_element = bin(int(element, base))[2:].zfill(size)
                # self.data.extend([bool(int(x)) for x in converted_element])
                for x in converted_element:
                    self.data.append(int(x))
                continue

            for c in element:
                self.data.extend([int(x) for x in bin(ord(c))[2:].zfill(size)])

        return starting_address, self.size - starting_address

    def modify_data(self, starting_bit = 0, list_of_new_bits : list = []):
        try:
            for i, bit in enumerate(list_of_new_bits):
                self.data[starting_bit + i] = int(bit)
        except IndexError:
            raise ModificationOutsideDataSection
        except ValueError:
            raise ValueIsNotANumber(f"Value '{bit}' cannot be converted to 0 or 1")

    def get_data(self, starting_bit = 0, length = 1, size = 8):

        size /= 8

        try:
            start = starting_bit * 8
            end = start + length * 8
            return self.data[start : end]
        except IndexError:
            raise SegmentationFault

    def get_data_as_str(self, starting_bit = 0, length = 1,  size = 8):
        return "".join(str(c) for c in self.get_data(starting_bit, length, size))
