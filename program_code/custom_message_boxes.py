"""
This file contains functions for displaying custom messages to the user
"""

from PyQt6.QtWidgets import QMessageBox
import json

with open('program_code/configs/names.json') as f:
    all_conumicates = json.load(f)
    supported_languages = all_conumicates["supported_languages"]
    lang_names_each_other = all_conumicates["lang_names_each_other"]
    names = all_conumicates["language_presets"]

ok_button =     QMessageBox.StandardButton.Ok
cancel_button = QMessageBox.StandardButton.Cancel

#
#   File Errors
#

def _1(**kwargs):
    """Selected file doesn't exist, or cannot be reached or read"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["file_doesnt_exist"])
    msg.setText(names[language]["file_not_sel_try_again"])
    msg.setStandardButtons(ok_button | cancel_button)
    return msg.exec()

def _2(**kwargs):
    """Selected file have size >= 1MB"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["file_too_big"])
    msg.setText(names[language]["file_size_warning"])
    msg.addButton(names[language]["sel_new_file"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cont_this_file"], QMessageBox.ButtonRole.NoRole) # returns 3
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)     # returns 4
    return msg.exec()

def _3(**kwargs):
    """File type is not .asm"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["improper_file_type"])
    msg.setText(names[language]["wrong_file_extension"])
    msg.addButton(names[language]["sel_new_file"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cont_this_file"], QMessageBox.ButtonRole.NoRole) # returns 3
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)     # returns 4
    return msg.exec()

#
#   Preprocessing Errors
#

def _4(**kwargs):
    """This error occurs if during preprocessing line containing only colon is detected"""
    language = kwargs["language"]
    line = kwargs["line"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["data_sec_error"])
    msg.setText(names[language]["label_line_empty"] + f"\nLine: {line}")
    return msg.exec()

def _4_question(**kwargs):
    """This error occurs if during preprocessing line containing only colon is detected"""
    language = kwargs["language"]
    line = kwargs["line"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["data_sec_error"])
    msg.setText(names[language]["label_line_empty"] + f"\nLine: {line}")
    msg.addButton(names[language]["load_interactive"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)         # returns 4
    return msg.exec()

def _5(**kwargs):
    """This error occurs if during preprocessing, multiple colons in line are detected"""
    language = kwargs["language"]
    line = kwargs["line"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["multiple_colons"])
    msg.setText(names[language]["too_many_colons"] + f"\nLine: {line}")
    return msg.exec()

def _5_question(**kwargs):
    """This error occurs if during preprocessing, multiple colons in line are detected"""
    language = kwargs["language"]
    line = kwargs["line"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["multiple_colons"])
    msg.setText(names[language]["too_many_colons"] + f"\nLine: {line}")
    msg.addButton(names[language]["load_interactive"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)         # returns 4
    return msg.exec()

def _6(**kwargs):
    """This error occurs if during preprocessing, improper use of : was detected"""
    language = kwargs["language"]
    line = kwargs["line"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["improper_line"])
    msg.setText(names[language]["improper_colon"] + f"\nLine: {line}")
    return msg.exec()

def _6_question(**kwargs):
    """This error occurs if during preprocessing, improper use of : was detected"""
    language = kwargs["language"]
    line = kwargs["line"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["improper_line"])
    msg.setText(names[language]["improper_colon"] + f"\nLine: {line}")
    msg.addButton(names[language]["load_interactive"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)         # returns 4
    return msg.exec()

def _7(**kwargs):
    """This error occurs if an unsupported section is detected in interactive mode"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["unrecognized_section"])
    msg.setText(names[language]["improper_section"])
    return msg.exec()

def _7_question(**kwargs):
    """This error occurs if an unsupported section is detected in interactive mode"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["unrecognized_section"])
    msg.setText(names[language]["improper_section"])
    msg.addButton(names[language]["load_interactive"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)         # returns 4
    return msg.exec()

def _8(**kwargs):
    """This error occurs if during preprocessing variable with improper name is detected"""
    language = kwargs["language"]
    line = kwargs["line"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["data_sec_error"])
    msg.setText(names[language]["incorrect_var_name"] + f"\nLine: {line}")
    return msg.exec()

def _8_question(**kwargs):
    """This error occurs if during preprocessing variable with improper name is detected"""
    language = kwargs["language"]
    line = kwargs["line"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["data_sec_error"])
    msg.setText(names[language]["incorrect_var_name"] + f"\nLine: {line}")
    msg.addButton(names[language]["load_interactive"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)         # returns 4
    return msg.exec()

def _9(**kwargs):
    """This error occurs if during preprocessing when improperly defined variable is detected"""
    language = kwargs["language"]
    line = kwargs["line"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["data_sec_error"])
    msg.setText(names[language]["variable_wrongly_defined"] + f"\nLine: {line}")
    return msg.exec()

def _9_question(**kwargs):
    """This error occurs if during preprocessing when improperly defined variable is detected"""
    language = kwargs["language"]
    line = kwargs["line"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["data_sec_error"])
    msg.setText(names[language]["variable_wrongly_defined"] + f"\nLine: {line}")
    msg.addButton(names[language]["load_interactive"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)         # returns 4
    return msg.exec()

#
#   Engine Errors
#

def _10(**kwargs):
    """Detected instruction is not supported"""
    language = kwargs["language"]
    line = kwargs["line"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["unsuported_instruction"])
    msg.setText(names[language]["is_valid_supported"])
    return msg.exec()

def _11(**kwargs):
    """Argument wasn't recognized to be anything supported"""
    language = kwargs["language"]
    line = kwargs["line"]
    values = kwargs["values"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["argument_unrecognized"])
    msg.setText(names[language]["arg_not_recognized"] + "\n" +
                names[language]["line"] + ": " + str(line) + "\n" + 
                names[language]["err_by"] + ": " + str(values))
    return msg.exec()

def _12(**kwargs):
    """Unrecognized element in memory call"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["mem_call_error"])
    msg.setText(names[language]["undef_elem_mem_call"])
    return msg.exec()

def _13(**kwargs):
    """Double memory call in one instruction - that's not allowed"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["double_mem_ref"])
    msg.setText(names[language]["double_mem_call_not_all"])
    return msg.exec()

def _14(**kwargs):
    """Multiple register call in one instruction - that's not allowed"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["more_than_two_vars"])
    msg.setText(names[language]["too_many_reg_calls"])
    return msg.exec()

def _15(**kwargs):
    """Multiple register call in one instruction - that's not allowed"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["use_reg_once"])
    msg.setText(names[language]["same_reg_used_twice"])
    return msg.exec()

def _16(**kwargs):
    """It's only possible to use BX, BP, DI, SI registers in memory call"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["curimc"])
    msg.setText(names[language]["otrcbu"])
    return msg.exec()

def _17(**kwargs):
    """Two registers with the same type - ex. BX & DX"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["two_reg_same_type"])
    msg.setText(names[language]["ret_same_type"])
    return msg.exec()

def _18(**kwargs):
    """Unrecognized element in complex value"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["compl_val_error"])
    msg.setText(names[language]["calc_val_failed"])
    return msg.exec()

def _23(**kwargs):
    """Instruction contains two mismatched explicite sizes definitions"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["expli_size_diff"])
    msg.setText(names[language]["expli_size_mimatch"])
    return msg.exec()

def _24(**kwargs):
    """Instruction with args memory & value require explicite size def. for at
    least one of it's parameters"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["no_explicite_size"])
    msg.setText(names[language]["no_size_in_inst"])
    return msg.exec()

def _25(**kwargs):
    """Not possible to call memory twice in one instruction"""
    
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["ill_doub_mem"])
    msg.setText(names[language]["ill_to_use_mem_call_twice"])
    return msg.exec()

def _26(**kwargs):
    """Can't execute function with two arguments, with first being value"""
    
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["val_not_dest"])
    msg.setText(names[language]["not_poss_to_save_to_val"])
    return msg.exec()

def _27(**kwargs):
    """Can't execute specific function with passed number of parameters"""

    language = kwargs["language"]
    param_no = kwargs["param_no"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["wrong_no_params"])
    msg.setText(names[language]["incorrect_no_of_params"] + f"\n'{param_no}'")
    return msg.exec()

def _28(**kwargs):
    """Can't execute specific function with this combination of parameters"""
    
    language = kwargs["language"]
    params = kwargs["params"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["wrong_param_types"])
    msg.setText(names[language]["param_comb_not_all"] + f"\n{params}")
    return msg.exec()

def _29(**kwargs):
    """While running instruction an error occurred"""
    language = kwargs["language"]
    line = kwargs["line"]
    source_error = kwargs["source_error"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["instruction_error"])
    msg.setText(names[language]["processing_error"] + "\n" +
                names[language]["line"] + ": " + str(line) + "\n" +
                str(source_error))
    return msg.exec()

#
#   Instruction Error
#

def _30(**kwargs):
    """This error occurs if sign doesn't match expected value in IDIV operaiton"""

    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["usidiv"])
    msg.setText(names[language]["sintoeidiv"])
    return msg.exec()

def _31(**kwargs):
    """This error occurs if in bit movement instruction shift value is passed in
    register other than CL"""

    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["ocla"])
    msg.setText(names[language]["occbu"])
    return msg.exec()

def _32(**kwargs):
    """This error occurs if in bit movement instruction shift value is passed in
    immediate value other than 1"""

    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["cuht1"])
    msg.setText(names[language]["cuovt1"])
    return msg.exec()

#
#   GUI Errors
#

def _40(**kwargs):
    """User tried to load empty file, or file containing only white characters"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["no_instructions"])
    msg.setText(f"{names[language]['nothing_to_do']}")
    return msg.exec()

def _40_question(**kwargs):
    """User tried to load empty file, or file containing only white characters"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["empty_file"])
    msg.setText(f"{names[language]['empty_file_detected']}")
    msg.addButton(names[language]["load_interactive"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)         # returns 4
    return msg.exec()

def _41(**kwargs):
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["value_not_allowed"])
    msg.setText(names[language]["only_binary_value"])
    return msg.exec()

def _42(**kwargs):
    """Binary number containing other chars other than 1's and 0's"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["invalid_binary_number"])
    msg.setText(names[language]["only_1_0_allowed"])
    return msg.exec()

def _43(**kwargs):
    """Inputed value cannot be converted to decimal"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["value_not_allowed"])
    msg.setText(names[language]["invalid_decimal"])
    return msg.exec()

def _44(**kwargs):
    """Decimal value outside boundaries for 8-bit binary number"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["value_not_allowed"])
    msg.setText(names[language]["value_0_255"])
    return msg.exec()

def _45(**kwargs):
    """Decimal value outside boundaries for 8-bit binary number"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["value_not_allowed"])
    msg.setText(names[language]["decimal_num_oor"])
    return msg.exec()

def _46(**kwargs):
    """Binary number representing outside range of 00000000-11111111"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["value_not_allowed"])
    msg.setText(names[language]["binary_num_oor_8"])
    return msg.exec()

def _47(**kwargs):
    """Binary number representing outside range of 0000000000000000-1111111111111111"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["value_not_allowed"])
    msg.setText(names[language]["binary_num_oor_16"])
    return msg.exec()

def _48(**kwargs):
    """It's not possible to edit name of variable at runtime"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["operation_forbidden"])
    msg.setText(names[language]["cannot_edit_name"])
    return msg.exec()

def _49(**kwargs):
    """It's not possible to edit address of variable at runtime"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["operation_forbidden"])
    msg.setText(names[language]["cant_edit_address"])
    return msg.exec()

def _50(**kwargs):
    """It's not possible to edit size of variable at runtime"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["operation_forbidden"])
    msg.setText(names[language]["cannot_edit_size"])
    return msg.exec()

def _51(**kwargs):
    """It's not possible to edit format of variable at runtime"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["operation_forbidden"])
    msg.setText(names[language]["cannot_edit_format"])
    return msg.exec()

#
#   Warnings
#

def _value_exceeds_bound(**kwargs):
    """Defined value is too big for the destination - additional values are ignored"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["value_too_big"])
    msg.setText(names[language]["val_exceeds_bounds"])
    return msg.exec()

def _explicite_size_ignored(**kwargs):
    """Instruction with arguments memory & register ignores explicite size if it's
    greater than the register itself"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["expli_size_ign"])
    msg.setText(names[language]["why_expli_siz_ign"])
    return msg.exec()

#
#   Undefined Error
#

def _60(**kwargs):
    """An undefined error occurred"""
    language = kwargs["language"]
    source_error = kwargs["source_error"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["unhandled_exception"])
    msg.setText(f"{names[language]['original_error']}:\n{source_error}")
    return msg.exec()

################################################################################

all_popups = locals()

def show_custom_popup(language : str, notification : dict) -> int:
    
    popup        = "_" + notification["popup"]
    line         = notification.get("line", None)
    param_no     = notification.get("param_no")
    params       = notification.get("params")
    values       = notification.get("values")
    source_error = notification.get("source_error")

    if line and type(line) == list:    line = line[0]

    if type(params) == list:
        params_list = []
        for par in params:
            params_list.append(names[language][f"param_{par}"])
        connector = names[language]["connector"]
        params_adjusted = f"{connector}".join(params_list)
    else:
        params_adjusted = names[language]["no_params"]

    if popup in all_popups:
        return all_popups[popup](language = language, 
                                 line = line,
                                 param_no = param_no, 
                                 params = params_adjusted,
                                 values = values,
                                 source_error = source_error)
