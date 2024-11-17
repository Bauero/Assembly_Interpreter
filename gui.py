"""
This file contains main funciton responsible for handling a gui app
"""
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget,
    QStackedLayout,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QHBoxLayout,
    QTextEdit,
    QComboBox
)
from custom_gui_elements import *
from errors import FileDoesntExist, FileSizeMightBeTooBig, FileTypeNotAllowed

class MainWindow(QWidget):
    """
    This class represents the main window. It stores all information about layout and functions
    which update the app depending on action by the user.
    """

    def __init__(self, code_handler):
        super().__init__()
        self.code_handler = code_handler
        self._createUserInterface()

    def _createUserInterface(self):
        """This funciton creates whole UI interface"""

        #   General settings
        self.setWindowTitle('Interpreter Asemblera')
        self.setGeometry(100, 200, 600, 400)

        #   Main widow structure
        main_window = QVBoxLayout()
        self.setLayout(main_window)
        self.pagesStack = QStackedLayout()

        #   Initialize all pages
        self._createMainMenuPage()
        self._createMainProgramPage()
        main_window.addLayout(self.pagesStack)

    def _createMainMenuPage(self):
        """Defines Main Menu page visible when user lanuches program"""
            
        #   Constants
        alg_cent = Qt.AlignmentFlag.AlignCenter
        font = QFont()
        font.setPointSize(20)

        #   Create base widget
        self.welcomeScreen = QWidget()
        welcomeLayout = QVBoxLayout()
        welcomeLayout.setAlignment(alg_cent)

        #   Create nested widget just for buttons
        self.welcomeScreenButtons = QWidget()
        welcomeButtonsLayout = QVBoxLayout()
        welcomeButtonsLayout.setAlignment(alg_cent)
        
        #   Defining properties of elemetns
        load_file_button = QPushButton('Wczytaj plik')
        load_file_button.clicked.connect(self.select_file_to_open_dialog)
        open_session_button = QPushButton('Tryb interakwyny')
        open_session_button.clicked.connect(self.open_interactive_mode)
        title = QLabel('Menu główne')
        title.setFont(font)

        #   Put elements in widgets
        welcomeLayout.addWidget(title, alignment = alg_cent)
        welcomeLayout.addWidget(QLabel(), alignment = alg_cent)
        welcomeButtonsLayout.addWidget(load_file_button, alignment = alg_cent)
        welcomeButtonsLayout.addWidget(open_session_button, alignment = alg_cent)

        #   Save layouts so that they can be displayed
        self.welcomeScreenButtons.setLayout(welcomeButtonsLayout)
        welcomeLayout.addWidget(self.welcomeScreenButtons)
        self.welcomeScreen.setLayout(welcomeLayout)
        self.pagesStack.addWidget(self.welcomeScreen)
        
    def _createMainProgramPage(self):
        """Designs the program page - live interpreter"""

        # Main container of the page
        self.programScreen = QWidget()
        programLayout = QVBoxLayout()
        self.programScreen.setLayout(programLayout)

        # Central container with registers and code
        self.centerSection = QWidget()
        centralLayout = QHBoxLayout()
        self.centerSection.setLayout(centralLayout)

        # Left column of the page
        self.leftSection = QWidget()
        leftSectionLayout = QFormLayout()
        leftSectionLayout.setAlignment(alg_top)

        # Right column of the page
        self.rightSection = QWidget()
        rightSectionLayout = QFormLayout()

        # Add widgets to the left section
        leftSectionLayout.addWidget(MultipurposeRegister("EAX", "#3099FF", 'Arithmetic & general purpose'))
        leftSectionLayout.addWidget(MultipurposeRegister("EBX", "#3099FF", 'Used for memory & general purpose'))
        leftSectionLayout.addWidget(MultipurposeRegister("ECX", "#3099FF", 'Counter & general purpose register'))
        leftSectionLayout.addWidget(MultipurposeRegister("EDX", "#3099FF"))
        leftSectionLayout.addWidget(FunctionalRegisters("ESI", 'orange'))
        leftSectionLayout.addWidget(FunctionalRegisters("EDI", 'orange'))
        leftSectionLayout.addWidget(FunctionalRegisters("ESP", 'orange', 'Stack Index Register - \'top\' position where new data will be stored by default'))
        leftSectionLayout.addWidget(FunctionalRegisters("EBP", 'orange', 'Points to the base of stack'))
        leftSectionLayout.addWidget(FunctionalRegisters("IP", "#CC3F0C"))
        leftSectionLayout.addWidget(FlagRegister())

        self.leftSection.setLayout(leftSectionLayout)
        centralLayout.addWidget(self.leftSection)

        # Create control buttons in right seciton
        self.nextLineButton = QPushButton('Następna linia')
        self.previousLineButton = QPushButton('Poprzednia linia')
        self.showVariables = QPushButton('Pokaż zmienne')

        self.startExecutionButton = QPushButton('Start')
        self.pauseExecutionButton = QPushButton('Pauza')
        self.saveStateButton = QPushButton('Zapisz stan')
        
        self.startAutoExecButton = QPushButton('Automatyczna egzeukcja kodu')
        comboBoxLabel = QLabel('Częstotliwosć wykonywania komend')
        self.executionFrequencyList = QComboBox()
        self.executionFrequencyList.addItem('0.1s')
        self.executionFrequencyList.addItem('0.5s')
        self.executionFrequencyList.addItem('1s')
        self.executionFrequencyList.addItem('2s')
        self.executionFrequencyList.addItem('5s')
        self.executionFrequencyList.setCurrentIndex(2)

        # Combine buttons into rows for right column
        row_1 = QHBoxLayout()
        row_1.addWidget(self.nextLineButton)
        row_1.addWidget(self.previousLineButton)
        row_1.addWidget(self.showVariables)

        row_2 = QHBoxLayout()
        row_2.addWidget(self.startExecutionButton)
        row_2.addWidget(self.pauseExecutionButton)
        row_2.addWidget(self.saveStateButton)

        row_3 = QHBoxLayout()
        row_3.addWidget(self.startAutoExecButton)
        row_3.addWidget(comboBoxLabel)
        row_3.addWidget(self.executionFrequencyList)

        # Add widgets to the right section
        code_field = QTextEdit('')
        code_field.setMinimumWidth(400)
        rightSectionLayout.addRow(code_field)
        rightSectionLayout.addRow(row_1)
        rightSectionLayout.addRow(row_2)
        rightSectionLayout.addRow(row_3)
        self.rightSection.setLayout(rightSectionLayout)
        centralLayout.addWidget(self.rightSection)

        # Add the central section to the main layout
        programLayout.addWidget(self.centerSection)

        # Add the terminal at the bottom of the main layout
        self.terminal = Terminal()
        programLayout.addWidget(self.terminal)  # Add terminal directly to programLayout

        # Add the program screen to the page stack
        self.pagesStack.addWidget(self.programScreen)
        
    ############################################################################
    #   Functions which will be called as an action of buttons
    ############################################################################

    @pyqtSlot()
    def select_file_to_open_dialog(self):
        """Propt user to select file & handles excptions"""

        ignore_size_limit   : bool = False
        ignore_file_type    : bool = False
        file_path = ''

        while True:
            if not file_path:
                file_path = QFileDialog.getOpenFileName(
                    self,
                    "Open File",
                    "${HOME}",
                    "All Files (*);; Python Files (*.py);; PNG Files (*.png)",
                )[0]

                if not file_path: return

            try:
                self.code_handler.loadFile(file_path, ignore_size_limit, ignore_file_type)
            except FileDoesntExist:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("File doesn't exist!")
                msg.setText("No file selected or file doesn't exist! 😵\nWant to try again?")
                msg.setStandardButtons(ok_button | cancel_button)
                ans = msg.exec()
                if ans == cancel_button.value:  return
                file_path = ''
                continue
            except FileSizeMightBeTooBig:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("File size might be too big")
                msg.setText("It seems you are trying to open file above 1MB in size! \nWhat do you want to do?")
                msg.addButton("Disable warning and select new file", QMessageBox.ButtonRole.YesRole)  # returns 2
                msg.addButton("Continue with this file", QMessageBox.ButtonRole.NoRole) # returns 3
                msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole) # returns 4
                ans = msg.exec()
                print(ans, type(ans))
                match ans:
                    case 2:
                        ignore_size_limit = True
                        file_path = ''
                    case 3:
                        ignore_size_limit = True
                    case 4:
                        return
                continue
            except FileTypeNotAllowed:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("File doesn't exist!")
                msg.setText("File type is not within allowed file typed (.s, .asm) \nWant do you want to do?")
                msg.addButton("Disable warning and select new file", QMessageBox.ButtonRole.YesRole)  # returns 2
                msg.addButton("Continue with this file", QMessageBox.ButtonRole.NoRole) # returns 3
                msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole) # returns 4
                ans = msg.exec()
                print(ans, type(ans))
                match ans:
                    case 2:
                        ignore_file_type = True
                        file_path = ''
                    case 3:
                        ignore_file_type = True
                    case 4:
                        return
                continue
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("File doesn't exist!")
                msg.setText(f"{e}")
                ans = msg.exec()
                return
            
            break

        self.pagesStack.setCurrentIndex(1)
        
    @pyqtSlot()
    def open_interactive_mode(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Opcja niedostępna")
        msg.setText("Ta funkcjonalność jeszcze nie została dodana")
        msg.setStandardButtons(ok_button)
        ans = msg.exec()

    def executeCommand(self, command):
        try:
            output = self.code_handler.executeCommand(command)
        except Exception as e:
            ...


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    from engine import Engine
    from code_handler import CodeHandler

    app = QApplication([])
    engine = Engine()
    code_handeler = CodeHandler(engine)
    window = MainWindow(code_handeler)
    window.show()
    window.pagesStack.setCurrentIndex(1)
    sys.exit(app.exec())