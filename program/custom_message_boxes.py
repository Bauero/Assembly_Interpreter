from PyQt6.QtWidgets import QMessageBox

ok_button =     QMessageBox.StandardButton.Ok
cancel_button = QMessageBox.StandardButton.Cancel

def unrecognized_error_popup(e):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("File doesn't exist!")
    msg.setText(f"{e}")
    return msg.exec()

def file_doesnt_exist_popup():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("File doesn't exist!")
    msg.setText("No file selected or file doesn't exist! 😵\nWant to try again?")
    msg.setStandardButtons(ok_button | cancel_button)
    return msg.exec()

def file_size_too_big():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("File size might be too big")
    msg.setText("It seems you are trying to open file above 1MB in size! \nWhat do you want to do?")
    msg.addButton("Disable warning and select new file", QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton("Continue with this file", QMessageBox.ButtonRole.NoRole) # returns 3
    msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole) # returns 4
    return msg.exec()

def improper_file_type():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("File doesn't exist!")
    msg.setText("File type is not within allowed file typed (.s, .asm) \nWant do you want to do?")
    msg.addButton("Disable warning and select new file", QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton("Continue with this file", QMessageBox.ButtonRole.NoRole) # returns 3
    msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole) # returns 4
    return msg.exec()

def preparation_error(e):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("Preprocessing error")
    msg.setText(f"Wrong data definition:\nLine {e.line()}\nMessage: \"{e.message()}\"")
    msg.addButton("Load file in interactive mode", QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole) # returns 4
    return msg.exec()

def preprocessing_error(e):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("Preprocessing error")
    msg.setText(f"Improper line marker definition:\nLine {e.line()}\nMessage: \"{e.message()}\"")
    msg.addButton("Load file in interactive mode", QMessageBox.ButtonRole.YesRole)  # returns 2
    msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole) # returns 4
    return msg.exec()
