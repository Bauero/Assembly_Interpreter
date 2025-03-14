
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

-------

# Układ plików programu (Program's files organization)

```
Assembly_interpreter
├─ README.md
├─ requirements.txt
├─ main.py
└─ program_code
   ├─ __init__.py
   ├─ assembly_instructions
   │  ├─ __init__.py
   │  ├─ arithmetic_instrunctions.py
   │  ├─ bit_movement_instructions.py
   │  ├─ data_movement_instructions.py
   │  ├─ flag_setting_instructions.py
   │  ├─ flow_control_instructions.py
   │  ├─ interrupt_instructions.py
   │  ├─ jump_instructions.py
   │  ├─ logical_instrunctions.py
   │  └─ stack_instructions.py
   ├─ code_handler.py
   ├─ code_warnings.py
   ├─ configs
   │  ├─ color_palette.json
   │  └─ names.json
   ├─ custom_gui_elements.py
   ├─ custom_message_boxes.py
   ├─ engine.py
   ├─ errors.py
   ├─ flag_register.py
   ├─ gui.py
   ├─ hardware_memory.py
   ├─ hardware_registers.py
   ├─ helper_functions.py
   ├─ history.py
   └─ preprocessor.py
```


