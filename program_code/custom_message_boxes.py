from PyQt6.QtWidgets import QMessageBox
import json

with open('program_code/names.json') as f:
    names = json.load(f)

ok_button =     QMessageBox.StandardButton.Ok
cancel_button = QMessageBox.StandardButton.Cancel

def unrecognized_error_popup(language : str, e : Exception) -> int:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["unhandled_exception"])
    msg.setText(f"{names[language]['original_error']}:\n{e}")
    return msg.exec()

def file_doesnt_exist_popup(language : str) -> int:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["file_doesnt_exist"])
    msg.setText(names[language]["file_not_sel_try_again"])
    msg.setStandardButtons(ok_button | cancel_button)
    return msg.exec()

def file_size_too_big(language : str) -> int:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["file_too_big"])
    msg.setText(names[language]["file_size_warning"])
    msg.addButton(names[language]["sel_new_file"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cont_this_file"], QMessageBox.ButtonRole.NoRole) # returns 3
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)     # returns 4
    return msg.exec()

def improper_file_type(language : str) -> int:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["improper_file_type"])
    msg.setText(names[language]["wrong_file_extension"])
    msg.addButton(names[language]["sel_new_file"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cont_this_file"], QMessageBox.ButtonRole.NoRole) # returns 3
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)     # returns 4
    return msg.exec()

def data_section_error(language : str, e : Exception) -> int:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(names[language]["data_sec_error"])
    msg.setText(f"{names[language]['incorrect_data_def']}")
    msg.addButton(names[language]["load_interactive"], QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton(names[language]["cancel"], QMessageBox.ButtonRole.RejectRole)         # returns 4
    return msg.exec()

def improper_label_error(language : str, e : Exception) -> int:
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
    msg.exec()


