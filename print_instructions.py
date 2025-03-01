"""
This file generates .md files for all instructions which are available in interpreter

One should copy this file into main catalogue and run it using
`python3.11 print_instructions.py`
"""

import os
from assembly_instructions.arithmetic_instrunctions import *
from assembly_instructions.flag_setting_instructions import *
from assembly_instructions.logical_instrunctions import *
from assembly_instructions.flow_control_instructions import *
from assembly_instructions.jump_instructions import *
from assembly_instructions.stack_instructions import *
from assembly_instructions.data_movement_instructions import *

for fn_name in list(filter(lambda n: n.upper() == n, dir())):
    fn = locals()[fn_name]
    comment = str(fn.__doc__).replace('\t','').replace('    ', '')
    if not os.path.exists("./Instructions and descriptions"):
        os.mkdir("./Instructions and descriptions")
    with open(rf"./Instructions and descriptions/{fn_name.upper()}.md", "w") as f:
        f.write(comment)
