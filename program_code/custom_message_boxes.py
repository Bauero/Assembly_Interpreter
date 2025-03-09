from PyQt6.QtWidgets import QMessageBox
import json

with open('program_code/names.json') as f:  names = json.load(f)

ok_button =     QMessageBox.StandardButton.Ok
cancel_button = QMessageBox.StandardButton.Cancel


def _unrecognized_error_popup(**kwargs):
    """An undefined error occured"""
    language = kwargs["language"]
    source_error = kwargs["source_error"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["unhandled_exception"])
    msg.setText(f"{names[language]['original_error']}:\n{source_error}")
    return msg.exec()

#
#   Input File Errors
#

def _file_doesnt_exist_popup(**kwargs):
    """Selected file doesn't exist, or cannot be reached or read"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["file_doesnt_exist"])
    msg.setText(names[language]["file_not_sel_try_again"])
    msg.setStandardButtons(ok_button | cancel_button)
    return msg.exec()

def _file_size_too_big(**kwargs):
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

def _improper_file_type(**kwargs):
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

def _data_section_error(**kwargs):
    """An error was detected in data section"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["data_sec_error"])
    msg.setText(f"{names[language]['incorrect_data_def']}")
    msg.addButton(names[language]["load_interactive"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)         # returns 4
    return msg.exec()

#
#   GUI Errors
#

def _improper_label_error(**kwargs):
    """Incorrect label name detected during preprocessing of file"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["improper_label"])
    msg.setText(f"{names[language]['incorrect_label']}")
    msg.addButton(names[language]["load_interactive"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)         # returns 4
    return msg.exec()

def _improper_flags_value(**kwargs):
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["value_not_allowed"])
    msg.setText(names[language]["only_binary_value"])
    return msg.exec()

def _invalid_binary_number(**kwargs):
    """Binary number containg other chars other than 1's and 0's"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["invalid_binary_number"])
    msg.setText(names[language]["only_1_0_allowed"])
    return msg.exec()

def _incorrect_decimal_value(**kwargs):
    """Decimal value outside boundaries for 8-bit binary number"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["value_not_allowed"])
    msg.setText(names[language]["value_0_255"])
    return msg.exec()

def _cannot_edit_name(**kwargs):
    """It's not possible to edit name of variable at runtime"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["operation_forbidden"])
    msg.setText(names[language]["cannot_edit_name"])
    return msg.exec()

def _cannot_edit_address(**kwargs):
    """It's not possible to edit address of variable at runtime"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["operation_forbidden"])
    msg.setText(names[language]["cant_edit_address"])
    return msg.exec()

def _cannot_edit_size(**kwargs):
    """It's not possible to edit size of variable at runtime"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["operation_forbidden"])
    msg.setText(names[language]["cannot_edit_size"])
    return msg.exec()

def _cannot_edit_format(**kwargs):
    """It's not possible to edit format of variable at runtime"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["operation_forbidden"])
    msg.setText(names[language]["cannot_edit_format"])
    return msg.exec()

#
#   Engine Errors
#

def _unsuported_instruction(**kwargs):
    """Detected instruction is not supported"""
    language = kwargs["language"]
    line = kwargs["line"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["unsuported_instruction"])
    msg.setText(names[language]["is_valid_supported"])
    return msg.exec()

def _unrecognized_argument(**kwargs):
    """Argument wasn't recognized to be anything supported"""
    language = kwargs["language"]
    line = kwargs["line"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["argument_unrecognized"])
    msg.setText(names[language]["arg_not_recognized"] + "\n" +
                names[language]["line"] + ": " + str(line))
    return msg.exec()

def _instruction_error(**kwargs):
    """While running instruction an error occured"""
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

def _unrecognized_elem_mem_call(**kwargs):
    """Unrecognized element in memory call"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["mem_call_error"])
    msg.setText(names[language]["undef_elem_mem_call"])
    return msg.exec()

def _double_memory_reference(**kwargs):
    """Double memory call in one instruction - that's not allowed"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["double_mem_ref"])
    msg.setText(names[language]["double_mem_call_not_all"])
    return msg.exec()

def _multiple_register_reference(**kwargs):
    """Multiple register call in one instruction - that's not allowed"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["doublemany_reg_call_mem_ref"])
    msg.setText(names[language]["too_many_reg_calls"])
    return msg.exec()

def _register_called_twice(**kwargs):
    """Multiple register call in one instruction - that's not allowed"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["use_reg_once"])
    msg.setText(names[language]["same_reg_used_twice"])
    return msg.exec()

def _reg_same_type(**kwargs):
    """Two registers with the same type - ex. BX & DX"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["two_reg_same_type"])
    msg.setText(names[language]["ret_same_type"])
    return msg.exec()

def _first_reg_must_be_bx(**kwargs):
    """In memory call, first register must be bx if multipurpose reg is used on first
    position"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["wrong_first_reg"])
    msg.setText(names[language]["first_reg_bx"])
    return msg.exec()

def _cant_use_sp(**kwargs):
    """Not possible to use SP for memory call, as an only register or in expression"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["cant_use_sp"])
    msg.setText(names[language]["sp_not_callable"])
    return msg.exec()

def _unrecognized_value_compl_val(**kwargs):
    """Unrecognized element in complex value"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["compl_val_error"])
    msg.setText(names[language]["calc_val_failed"])
    return msg.exec()

def _no_explicite_size(**kwargs):
    """Instruction with args memory & value require explicite size def. for at
    least one of it's parameters"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["no_explicite_size"])
    msg.setText(names[language]["no_size_in_inst"])
    return msg.exec()

def _explicite_sizes_mismatch(**kwargs):
    """Instruction contains two mismatched explicite sizes definitions"""
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["expli_size_diff"])
    msg.setText(names[language]["expli_size_mimatch"])
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

def _cant_call_mem_twice(**kwargs):
    """Not possible to call memory twice in one instruction"""
    
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["ill_doub_mem"])
    msg.setText(names[language]["ill_to_use_mem_call_twice"])
    return msg.exec()

def _cant_call_mem_twice(**kwargs):
    """Can't execute function with two arguments, with first being value"""
    
    language = kwargs["language"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["val_not_dest"])
    msg.setText(names[language]["not_poss_to_save_to_val"])
    return msg.exec()

def _wrong_no_of_params(**kwargs):
    """Can't execute specific function with passed number of parameters"""

    language = kwargs["language"]
    param_no = kwargs["param_no"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["wrong_no_params"])
    msg.setText(names[language]["incorrect_no_of_params"] + f"\n'{param_no}'")
    return msg.exec()

def _wrong_combination_params(**kwargs):
    """Can't execute specific function with this combination of parameters"""
    
    language = kwargs["language"]
    params = kwargs["params"]
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["wrong_param_types"])
    msg.setText(names[language]["param_comb_not_all"] + f"\n{params}")
    return msg.exec()

################################################################################

all_popups = locals()

def show_custom_popup(language : str, notification : dict) -> int:
    
    popup        = "_" + notification["popup"]
    line         = notification["line"]
    param_no     = notification["param_no"]
    params       = notification["params"]
    source_error = notification["source_error"]

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
                                 source_error = source_error)
