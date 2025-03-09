"""
This file generates .md files for all instructions which are available in interpreter

One should copy this file into root folder for this project (the same folder in which `main.py` is
located) and execute:
- `python3.11 print_instructions.py`
"""

import os
from program_code import *
import inspect

functions = {name: obj for name, obj in inspect.getmembers(locals()["assembly_instructions"], inspect.isfunction)}
uppercase_functions = {name: func for name, func in functions.items() if name.isupper()}

for fn_name in uppercase_functions:
    fn = uppercase_functions[fn_name]
    comment = str(fn.__doc__).replace('\t','').replace('    ', '')
    if not os.path.exists("./Instructions and descriptions"):
        os.mkdir("./Instructions and descriptions")
    with open(rf"./Instructions and descriptions/{fn_name.upper()}.md", "w") as f:
        f.write(comment)
