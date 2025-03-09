
# O projekcie (About)
## PL
Ten projekt jest moją pracą inżynierską dotyczącą napisanego w Pythonie interpretera kodu Asembly 32bit w wersji NASM. Zadaniem programu jest wspomaganie użytkownika w nauce programowania w niskopoziomowym jezyku, Asembly poprzez dostarczenie mu narzędzi napisanym w jezyku wysokopoziomowym umożlilwiające analizę kodu z poziomu CLI oraz GUI i podejrzenie rezultatów.

### Założenia projektu
- Umożliwienie podlądania rezultatów wykonywania programu poprzez interfejs GUI / CLI
- Umożliwienie wykonywania pojedyńczych poleceń w trybie interaktywnym
- Wczytywanie projektu i wykonywanie kodu w nim zawartego
- Podpowiedzi odnośnie kodu
- Wykrywanie błędów

## EN
This project is my engineering thesis which topic is an Assembly 32-bit interpreter written in Python language. The goal is to provide user with help in learning low-level language like Assembly by giving tool for analysis and execution of code in high-level language in both GUI and CLI

### Project assumption
- Ability to preview result of code execution through GUI / CLI
- Ability to execute single comamdn in interactive mode
- Project loading and execution
- Hints about code
- Error detection


```
Assembly_interpreter
├─ Example assembly programs
│  ├─ incorrect_programs
│  │  ├─ ImproperJumpMarker.s
│  │  ├─ add_two_numbers.s
│  │  ├─ cant_use_sp.asm
│  │  ├─ illegal_operations.s
│  │  ├─ incorrect_file_type.txt
│  │  ├─ instruction_not_supported_error.asm
│  │  ├─ unrecognized_argument_error.asm
│  │  ├─ wrong_combination_params.asm
│  │  └─ wrong_param_types.asm
│  ├─ programs_EN
│  │  ├─ convert_calculate_RPN.asm
│  │  └─ show_time.asm
│  ├─ programs_PL
│  │  ├─ obliczanie_ONP_dzialania.asm
│  │  └─ pokaz_czas.asm
│  └─ test_programs
│     ├─ all_vaild_add_instructions.asm
│     ├─ all_valid_flag_setting_instructions.asm
│     ├─ infinite_loop.asm
│     ├─ jumps_and_labels.asm
│     ├─ test_pushes.asm
│     ├─ test_variable_section.asm
│     └─ working_stack.asm
├─ Extras
│  ├─ Implemented instructions
│  │  ├─ ADC.md
│  │  ├─ ADD.md
│  │  ├─ AND.md
│  │  ├─ CLC.md
│  │  ├─ CMC.md
│  │  ├─ CMP.md
│  │  ├─ DEC.md
│  │  ├─ INC.md
│  │  ├─ JA.md
│  │  ├─ JAE.md
│  │  ├─ JB.md
│  │  ├─ JBE.md
│  │  ├─ JC.md
│  │  ├─ JCXZ.md
│  │  ├─ JE.md
│  │  ├─ JG.md
│  │  ├─ JGE.md
│  │  ├─ JL.md
│  │  ├─ JLE.md
│  │  ├─ JMP.md
│  │  ├─ JNA.md
│  │  ├─ JNAE.md
│  │  ├─ JNB.md
│  │  ├─ JNBE.md
│  │  ├─ JNC.md
│  │  ├─ JNE.md
│  │  ├─ JNG.md
│  │  ├─ JNGE.md
│  │  ├─ JNL.md
│  │  ├─ JNLE.md
│  │  ├─ JNO.md
│  │  ├─ JNP.md
│  │  ├─ JNS.md
│  │  ├─ JNZ.md
│  │  ├─ JO.md
│  │  ├─ JP.md
│  │  ├─ JPE.md
│  │  ├─ JPO.md
│  │  ├─ JS.md
│  │  ├─ JZ.md
│  │  ├─ LOOP.md
│  │  ├─ LOOPE.md
│  │  ├─ LOOPNE.md
│  │  ├─ LOOPNZ.md
│  │  ├─ LOOPZ.md
│  │  ├─ MANUAL.md
│  │  ├─ MOV.md
│  │  ├─ NOT.md
│  │  ├─ OR.md
│  │  ├─ POP.md
│  │  ├─ POPA.md
│  │  ├─ POPF.md
│  │  ├─ PUSH.md
│  │  ├─ PUSHA.md
│  │  ├─ PUSHF.md
│  │  ├─ SBB.md
│  │  ├─ STC.md
│  │  ├─ SUB.md
│  │  ├─ XCHG.md
│  │  └─ XOR.md
│  └─ Utilities
│     ├─ flag_converter.py
│     └─ print_instructions.py
├─ README.md
├─ main.py
├─ open_gui.py
├─ program_code
│  ├─ __init__.py
│  ├─ assembly_instructions
│  │  ├─ __init__.py
│  │  ├─ arithmetic_instrunctions.py
│  │  ├─ bit_movement_instructions.py
│  │  ├─ data_movement_instructions.py
│  │  ├─ flag_setting_instructions.py
│  │  ├─ flow_control_instructions.py
│  │  ├─ interrupt_instructions.py
│  │  ├─ jump_instructions.py
│  │  ├─ logical_instrunctions.py
│  │  └─ stack_instructions.py
│  ├─ code_handler.py
│  ├─ code_warnings.py
│  ├─ color_palette.json
│  ├─ custom_gui_elements.py
│  ├─ custom_message_boxes.py
│  ├─ engine.py
│  ├─ errors.py
│  ├─ flag_register.py
│  ├─ gui.py
│  ├─ hardware_memory.py
│  ├─ hardware_registers.py
│  ├─ helper_functions.py
│  ├─ history.py
│  ├─ names.json
│  └─ preprocessor.py
├─ test.py
└─ test2.py

```