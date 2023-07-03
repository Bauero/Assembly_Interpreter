"""
The contents of this file is responsible for translating the command
from human readible line into peaces which whould be able to execute 
by the program
"""

import re

def lineCleanup(line : str) -> str | None:
    """
    chceck if string not empty and not comment -> lets it through
    """

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

def lineDecomposition(line : str) -> list:
    """
    Decomposition of line into order and arguments
    """
    
    # No possibility of line with sentence
    if not ("'" in line or '"' in line):
        
        splitted = []
        if "," in line:
            splitted = line.split(",")

        # Cleaning up white cha
        for e in range(len(splitted)):
            splitted[e] = splitted[e].strip()

        parts = []
        for elem in splitted:
            parts += elem.split(" ")

        for p in range(len(parts)-1,-1,-1):
            if parts[p] == "":
                parts.pop(p)

        return parts
    
    # There are ' or " in this line which suggest string
    else:
        (lap, rap, lq, rq) = (len(line), len(line), 0, 0)
        if "'" in line:
            lap = line.index("'")
            rap = line[-1::-1].index("'")
        if '"' in line:
            lq = line.index('"')
            rq = line[-1::-1].index('"')

        ul = min(lq, lap) # ultimate left start of string-like thing
        ur = max(rq, rap) # ultimate right end of string-like thing

        parts = line[:ul].split(" ") + [line[ul:ur+1]] + \
            line[ur:].split(" ")

        for p in range(len(parts)-1,-1,-1):
            if parts[p] == "":
                parts.pop(p)

        return parts
