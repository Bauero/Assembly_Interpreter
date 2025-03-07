from PyQt6.QtWidgets import QMessageBox
import json

with open('program_code/names.json') as f:  names = json.load(f)

ok_button =     QMessageBox.StandardButton.Ok
cancel_button = QMessageBox.StandardButton.Cancel

def unrecognized_error_popup(language : str, e : Exception) -> int:
    """An undefined error occured"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["unhandled_exception"])
    msg.setText(f"{names[language]['original_error']}:\n{e}")
    return msg.exec()

#
#   Input File Errors
#

def file_doesnt_exist_popup(language : str) -> int:
    """Selected file doesn't exist, or cannot be reached or read"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["file_doesnt_exist"])
    msg.setText(names[language]["file_not_sel_try_again"])
    msg.setStandardButtons(ok_button | cancel_button)
    return msg.exec()

def file_size_too_big(language : str) -> int:
    """Selected file have size >= 1MB"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["file_too_big"])
    msg.setText(names[language]["file_size_warning"])
    msg.addButton(names[language]["sel_new_file"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cont_this_file"], QMessageBox.ButtonRole.NoRole) # returns 3
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)     # returns 4
    return msg.exec()

def improper_file_type(language : str) -> int:
    """File type is not .asm"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["improper_file_type"])
    msg.setText(names[language]["wrong_file_extension"])
    msg.addButton(names[language]["sel_new_file"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cont_this_file"], QMessageBox.ButtonRole.NoRole) # returns 3
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)     # returns 4
    return msg.exec()

def data_section_error(language : str, e : Exception) -> int:
    """An error was detected in data section"""
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

def improper_label_error(language : str, e : Exception) -> int:
    """Incorrect label name detected during preprocessing of file"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["improper_label"])
    msg.setText(f"{names[language]['incorrect_label']}")
    msg.addButton(names[language]["load_interactive"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)         # returns 4
    return msg.exec()

def improper_flags_value(language : str) -> int:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["value_not_allowed"])
    msg.setText(names[language]["only_binary_value"])
    return msg.exec()

def invalid_binary_number(language : str) -> int:
    """Binary number containg other chars other than 1's and 0's"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["invalid_binary_number"])
    msg.setText(names[language]["only_1_0_allowed"])
    return msg.exec()

def incorrect_decimal_value(language : str) -> int:
    """Decimal value outside boundaries for 8-bit binary number"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["value_not_allowed"])
    msg.setText(names[language]["value_0_255"])
    return msg.exec()

def cannot_edit_name(language : str) -> int:
    """It's not possible to edit name of variable at runtime"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["operation_forbidden"])
    msg.setText(names[language]["cannot_edit_name"])
    return msg.exec()

def cannot_edit_address(language : str) -> int:
    """It's not possible to edit address of variable at runtime"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["operation_forbidden"])
    msg.setText(names[language]["cant_edit_address"])
    return msg.exec()

def cannot_edit_size(language : str) -> int:
    """It's not possible to edit size of variable at runtime"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["operation_forbidden"])
    msg.setText(names[language]["cannot_edit_size"])
    return msg.exec()

def cannot_edit_format(language : str) -> int:
    """It's not possible to edit format of variable at runtime"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(names[language]["operation_forbidden"])
    msg.setText(names[language]["cannot_edit_format"])
    return msg.exec()

#
#   Engine Errors
#

def unsuported_instruction(language : str) -> int:
    """Detected instruction is not supported"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["unsuported_instruction"])
    msg.setText(names[language]["is_valid_supported"])
    return msg.exec()

def unrecognized_argument(language : str, line : int) -> int:
    """Argument wasn't recognized to be anything supported"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["argument_unrecognized"])
    msg.setText(names[language]["arg_not_recognized"] + "\n" +
                names[language]["line"] + ": " + str(line))
    return msg.exec()

def instruction_error(language : str, line : int, source_err : Exception) -> int:
    """While running instruction an error occured"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["instruction_error"])
    msg.setText(names[language]["processing_error"] + "\n" +
                names[language]["line"] + ": " + str(line) + "\n" +
                str(source_err))
    return msg.exec()

def unrecognized_elem_mem_call(language : str) -> int:
    """Unrecognized element in memory call"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["mem_call_error"])
    msg.setText(names[language]["undef_elem_mem_call"])
    return msg.exec()

def double_memory_reference(language : str) -> int:
    """Double memory call in one instruction - that's not allowed"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["double_mem_ref"])
    msg.setText(names[language]["double_mem_call_not_all"])
    return msg.exec()

def multiple_register_reference(language : str) -> int:
    """Multiple register call in one instruction - that's not allowed"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["doublemany_reg_call_mem_ref"])
    msg.setText(names[language]["too_many_reg_calls"])
    return msg.exec()

def register_called_twice(language : str) -> int:
    """Multiple register call in one instruction - that's not allowed"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["use_reg_once"])
    msg.setText(names[language]["same_reg_used_twice"])
    return msg.exec()

def reg_same_type(language : str) -> int:
    """Two registers with the same type - ex. BX & DX"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["two_reg_same_type"])
    msg.setText(names[language]["ret_same_type"])
    return msg.exec()

def first_reg_must_be_bx(language : str) -> int:
    """In memory call, first register must be bx if multipurpose reg is used on first
    position"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["wrong_first_reg"])
    msg.setText(names[language]["first_reg_bx"])
    return msg.exec()

def cant_use_sp(language : str) -> int:
    """Not possible to use SP for memory call, as an only register or in expression"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["cant_use_sp"])
    msg.setText(names[language]["sp_not_callable"])
    return msg.exec()

def unrecognized_value_compl_val(language : str) -> int:
    """Unrecognized element in complex value"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["compl_val_error"])
    msg.setText(names[language]["calc_val_failed"])
    return msg.exec()

def no_explicite_size(language : str) -> int:
    """Instruction with args memory & value require explicite size def. for at
    least one of it's parameters"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["no_explicite_size"])
    msg.setText(names[language]["no_size_in_inst"])
    return msg.exec()

def explicite_sizes_mismatch(language : str) -> int:
    """Instruction contains two mismatched explicite sizes definitions"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["expli_size_diff"])
    msg.setText(names[language]["expli_size_mimatch"])
    return msg.exec()

def explicite_size_ignored(language : str) -> int:
    """Instruction with arguments memory & register ignores explicite size if it's
    greater than the register itself"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["expli_size_ign"])
    msg.setText(names[language]["why_expli_siz_ign"])
    return msg.exec()

def cant_call_mem_twice(language : str) -> int:
    """Not possible to call memory twice in one instruction"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["ill_doub_mem"])
    msg.setText(names[language]["ill_to_use_mem_call_twice"])
    return msg.exec()

def cant_call_mem_twice(language : str) -> int:
    """Can't execute function with two arguments, with first being value"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["val_not_dest"])
    msg.setText(names[language]["not_poss_to_save_to_val"])
    return msg.exec()

def wrong_no_of_params(language : str, param_no : int) -> int:
    """Can't execute specific function with passed number of parameters"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["wrong_no_params"])
    msg.setText(names[language]["incorrect_no_of_params"] + f"\n'{param_no}'")
    return msg.exec()

def wrong_combination_params(language : str, params : str) -> int:
    """Can't execute specific function with this combination of parameters"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["wrong_param_types"])
    msg.setText(names[language]["param_comb_not_all"] + f"\n{params}")
    return msg.exec()
