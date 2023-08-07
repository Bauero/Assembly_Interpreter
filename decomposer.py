"""
The contents of this file is responsible for translating the command
from human readible line into peaces which whould be able to execute 
by the program
"""

from errors import EmptyLine, ArgumentNotExpected, NotEnoughArguments, \
    TooManyArgumentsToUnpack

def lineCleanup(line : str, isText : bool = False) -> str | None:
    """
    Given a line of text, this function check if line is not empty
    and if so, does it contain anything else than a commment
    If true, function returns the remaingn part, else None
    
    line - line of document to cleanup
    isText - this flag might indicate that we are dealing with muliline
        text which happens to contain just en empty line

    ex.
    var word    "Intro

                outro$"

    In this example line shouldn't be remove at the beginning

    """
    
    # Empty line
    if len(line) == 0: return None
    
    nline = line.strip()

    # Only white characters
    if len(nline) == 0 and not isText: return None

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

def paramComparer(template : dict, values : list):
    """
    This function is responsible to detect, if the given parameters
    are in fact correctly put to the value - however, the function itself
    doesn't automatically check, if the parametres are correct (if the value
    is withing range, or if given parameter exist)

    INC 10 -> WRONG
    ADD AX,10 -> GOOD
    ADD AX,-18.5 -> GOOD !!!
    etc.
    """
    if len(values) == 1:
        command = values[0].upper()
    elif len(values) == 2:
        command, arg1 = values
    elif len(values) == 3:
        command, arg1, arg2 = values
    elif len(values) > 3:
        command, arg1, arg2, *args = values
    else:
        raise EmptyLine
    
    """
    The probem here, is that we can have ' ala dw "ala" ' , meanign assing
    to variable - what to do then?
    """



def functionAssigner(template : dict, values : list) -> dict:
    """
    If the given parammeters correspont to the signature of function
    ("visually" not gramatically), function would return a dictionary
    which would allow to execute function with paramteres
    EX: ADD AX, 10
    function = ADD
    arg1 = AX
    arg2 = 10
    """

    defaultArgumentsNumber = len(template.keys())
    givenArgumetnsNumber = len(values)

    if defaultArgumentsNumber == 0 and givenArgumetnsNumber > 0:
        raise ArgumentNotExpected

    elif defaultArgumentsNumber > givenArgumetnsNumber:
        raise NotEnoughArguments
    
    elif defaultArgumentsNumber < givenArgumetnsNumber:
        raise TooManyArgumentsToUnpack
    
    alignment = {}

    for k,i in zip(list(template.keys()),range(defaultArgumentsNumber)):
        alignment[k] = values[i]
    
    return alignment

def lineProcessing(line : str, tempalate : dict):
    """
    This function is the main line processing function
    it's purpose is to be an interface between engine, and
    function, which does preporcess the line and checks
    it's content and do work depending on what's inside
    """

    try:
        ...
    except EmptyLine:
        ...
    ...
