"""
The contents of this file is responsible for translating the command
from human readible line into peaces whic whould be able to execute 
by the program
"""

def preprocessing(line : str) -> any | None:

    # Empty line
    if len(line) == 0: return None
    
    nline = line.strip()

    # Only white characters
    if len(nline) == 0: return None

    # Only comment with white characters
    elif nline.startswith(";"): return None

    else:
        for c in range(len(nline)):
            if nline[c] == ';':
                nline = nline[:c]
                nline.strip()
                break
        
        return nline