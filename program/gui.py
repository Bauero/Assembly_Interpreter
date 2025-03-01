"""
This file contains main funciton responsible for handling a gui app
"""
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QHBoxLayout,
    QComboBox,
    QCheckBox,
    QSizePolicy
)
from .custom_gui_elements import *
from .errors import (FileDoesntExist,
                    FileSizeMightBeTooBig,
                    FileTypeNotAllowed,
                    ImproperJumpMarker,
                    ImproperDataDefiniton)
from .helper_functions import loadFileFromPath
from .color_pallete import *
from .custom_message_boxes import *
from screeninfo import get_monitors


class MainWindow(QWidget):
    """
    This class represents the main window. It stores all information about layout and functions
    which update the app depending on action by the user.
    """

    def __init__(self, code_handler):
        super().__init__()
        self.code_handler = code_handler
        self.interactive_mode = False
        self._createUserInterface()
        self._set_interactive_mode()
        self.program_running = False
        self.welcomeScreen.show()
        self.internal_timer = QTimer()
        self.timer_interval = 1000
        self.internal_timer.setInterval(self.timer_interval)
        self.internal_timer.stop()
        self.instructionCounter = 0

    def _createUserInterface(self):
        """This funciton creates whole UI interface"""

        monitor = get_monitors()[0]
        monitor_height, monitor_width = monitor.height, monitor.width
        w_heigth, w_width = monitor_height//4, monitor_width//4
        pos_x = monitor_width//2 - w_width//2
        pos_y = monitor_height//2 - w_heigth//2

        self._createMainMenuPage()
        self._createMainProgramPage()
        self.setWindowTitle('Interpreter Asemblera')
        self.welcomeScreen.setGeometry(pos_x, pos_y, w_width, w_heigth)
        self.programScreen.setGeometry(pos_x, pos_y, monitor_width, monitor_height)

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
        load_file_button.clicked.connect(self._select_file_to_open_dialog)
        open_session_button = QPushButton('Tryb interakwyny')
        open_session_button.clicked.connect(self._open_interactive_mode)
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
        
    def _createMainProgramPage(self):
        """Designs the program page - live interpreter"""

        self.programScreen = QWidget()
        programLayout = QVBoxLayout()
        self.programScreen.setLayout(programLayout)

        self.centerSection = QWidget()
        centralLayout = QHBoxLayout()
        self.centerSection.setLayout(centralLayout)

        font = QFont() ; font.setBold(True) ; font.setPointSize(15)
        
        #
        #   Registers Section
        #

        self.registersSection = QWidget()
        registersSectionLayout = QVBoxLayout()
        registersSectionLayout.setAlignment(alg_top)

        self.registers_label = QLabel("Registers")
        self.registers_label.setFont(font)
        registersSectionLayout.addWidget(self.registers_label)
        # registersSectionLayout.setStretch(10)

        HR = self.code_handler.engine.HR
        FR = self.code_handler.engine.FR
        self.register_section_elements = [
            MultipurposeRegister(HR, "AX", neon_blue, 'Arithmetic & general purpose'),
            MultipurposeRegister(HR, "BX", neon_blue, 'Used for memory & general purpose'),
            MultipurposeRegister(HR, "CX", neon_blue, 'Counter & general purpose register'),
            MultipurposeRegister(HR, "DX", neon_blue, 'Usef for memory, and buffor for some instrucitons like div'),
            FunctionalRegisters(HR, "SI", 'orange', "Source Index Register"),
            FunctionalRegisters(HR, "DI", 'orange', "Destination Index Register"),
            FunctionalRegisters(HR, "SP", 'orange', 'Stack Index Register - \'top\' position where new data will be stored by default'),
            FunctionalRegisters(HR, "BP", 'orange', 'Points to the base of stack'),
            FunctionalRegisters(HR, "IP", deep_red, "Instruction Pointer Register"),
            FlagRegister(FR)
        ]

        registersSectionLayout.setSpacing(0)

        for element in self.register_section_elements:
            element.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
            element.setMinimumHeight(50)  # Minimalna wysokość, do której może się skurczyć
            element.setMaximumHeight(120)
            registersSectionLayout.addWidget(element)

        self.registersSection.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        self.register_section_elements[-1].setMinimumHeight(130)
        self.registersSection.setLayout(registersSectionLayout)

        #
        #   Code and navigation buttons
        #

        self.codeSection = QWidget()
        codeSectionLayout = QFormLayout()
        code_label = QLabel("Code")
        code_label.setFont(font)
        self.code_field = CodeEditor()
        self.code_field.setMinimumWidth(400)

        self.nextLineButton         = QPushButton('Wykonaj instrukcję')
        self.previousLineButton     = QPushButton('Powrót do poprzedniej instrukcji')
        self.startExecutionButton   = QPushButton('Uruchom program')
        self.saveStateButton        = QPushButton('Zapisz stan')
        self.startAutoExecButton    = QCheckBox('Auto-wykonywanie')
        
        self.nextLineButton.        setEnabled(self.interactive_mode)
        self.previousLineButton.    setEnabled(self.interactive_mode)
        self.saveStateButton.       setEnabled(self.interactive_mode)
        self.startAutoExecButton.   setEnabled(True)
        self.startAutoExecButton.   setChecked(False)
        self.startAutoExecButton.   stateChanged.connect(lambda: self._run_next_instruction_or_stop())

        self.startExecutionButton.setStyleSheet(f"color: {light_green_color};")
        self.nextLineButton.clicked.        connect(lambda: self._executeCommand('next_instruction'))
        self.previousLineButton.clicked.    connect(lambda: self._executeCommand('previous_instruction'))
        self.startExecutionButton.clicked.  connect(lambda: self._executeCommand('start_stop'))
        self.saveStateButton.clicked.       connect(lambda: self._executeCommand('save_state'))
        
        comboBoxLabel = QLabel('Opóźnienie')
        comboBoxLabel.setAlignment(alg_right)
        self.executionFrequencyList = QComboBox()
        for t in ['0.25s', '0.5s', '1s', '2s', '5s']:
            self.executionFrequencyList.addItem(t)
        self.executionFrequencyList.setCurrentIndex(2)
        self.executionFrequencyList.currentIndexChanged.connect(self.on_frequency_change)
        
        box = QWidget()
        frequencyBox = QHBoxLayout()
        frequencyBox.addWidget(comboBoxLabel)
        frequencyBox.addWidget(self.executionFrequencyList)
        box.setLayout(frequencyBox)
        box

        row_1 = QHBoxLayout()
        row_1.addWidget(self.nextLineButton)
        row_1.addWidget(self.previousLineButton)

        row_2 = QHBoxLayout()
        row_2.addWidget(self.startExecutionButton)
        row_2.addWidget(self.saveStateButton)

        row_3 = QHBoxLayout()
        row_3.addWidget(self.startAutoExecButton)
        row_3.addWidget(box)

        codeSectionLayout.addRow(code_label)
        codeSectionLayout.setSpacing(10)
        codeSectionLayout.addRow(self.code_field)
        codeSectionLayout.addRow(row_1)
        codeSectionLayout.addRow(row_2)
        codeSectionLayout.addRow(row_3)
        self.codeSection.setLayout(codeSectionLayout)

        #
        #   Stack Section
        #

        self.stackColumn = QVBoxLayout()
        stack_label = QLabel("Stack")
        stack_label.setFont(font)
        DT = self.code_handler.engine.data
        self.stackSection = StackTable(DT)
        self.stackSection.setFixedWidth(190)
        self.stackSection.set_allow_change_content(False)
        self.stackSection.generate_table()
        self.stackColumn.addWidget(stack_label)
        self.stackColumn.addSpacing(10)
        self.stackColumn.addWidget(self.stackSection)
        
        #
        #   Variable section
        #

        self.variableColumn = QVBoxLayout()
        variables_label = QLabel("Variables")
        variables_label.setFont(font)
        engine = self.code_handler.engine
        self.variableSection = VariableTable(engine)
        self.variableColumn.addWidget(variables_label)
        self.variableColumn.addSpacing(10)
        self.variableColumn.addWidget(self.variableSection)

        #
        #   Terminal
        #

        self.terminal_widget = QWidget()
        self.terminal_layout = QVBoxLayout()

        self.terminal_label = QLabel('Terminal')
        font = QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.terminal_label.setFont(font)

        self.terminal = Terminal()
        self.terminal_layout.addWidget(self.terminal_label)
        self.terminal_layout.addWidget(self.terminal)
        self.terminal_widget.setLayout(self.terminal_layout)
        self.terminal_widget.setMaximumHeight(300)

        #
        #   Add elements to central layout
        #

        centralLayout.addWidget(self.registersSection, 1)
        centralLayout.addWidget(self.codeSection, 3)
        centralLayout.addLayout(self.stackColumn, 2)
        centralLayout.addLayout(self.variableColumn, 2)
        programLayout.addWidget(self.centerSection)
        programLayout.addWidget(self.terminal_widget)
        programLayout.setSpacing(0)

    ############################################################################
    #   Functions which will be called as an action of buttons
    ############################################################################

    @pyqtSlot()
    def _set_active_state(self, state = False):
        self.code_field.setDisabled(not state)
        self.stackSection.setDisabled(not state)
        self.variableSection.setDisabled(not state)

        for element in self.register_section_elements:
            element.setDisabled(not state)

        self.terminal_widget.setDisabled(not state)
        self.startExecutionButton.setDisabled(False)
        self.registers_label.setDisabled(False)
        self.terminal_label.setDisabled(False)
        self.registers_label.setDisabled(False)
        self.terminal_label.setVisible(True)
        self.terminal_label.setEnabled(True)

    @pyqtSlot()
    def _set_interactive_mode(self, interactive_active : bool = False):
        for element in self.register_section_elements:
            setattr(self, element.get_name(), element)
            element.set_interactive(interactive_active)

    @pyqtSlot()
    def on_frequency_change(self):
        selected_value = self.executionFrequencyList.currentIndex()
        interval = 0
        match selected_value:
            case 0:     interval = 250
            case 1:     interval = 500
            case 2:     interval = 1000
            case 3:     interval = 2000
            case 4:     interval = 5000
        self.internal_timer.setInterval(interval)
        self.timer_interval = interval

    @pyqtSlot()
    def _select_file_to_open_dialog(self):
        """Propt user to select file & handles excptions"""

        ignore_size_limit   : bool = False
        ignore_file_type    : bool = False
        file_path = ''

        while True:
            if not file_path:
                file_path = QFileDialog.getOpenFileName(
                    self, "Open File", "${HOME}",
                    "All Files (*);; Python Files (*.py);; PNG Files (*.png)",
                )[0]
                if not file_path: return

            try:
                lines = self.code_handler.readPrepareFile(file_path, ignore_size_limit, ignore_file_type)
                self.code_field.setText( self.code_handler.gcefat() )
                self.code_field.setHighlight(lines)
                self.code_field.setEditable(False)
            except FileDoesntExist:
                ans = file_doesnt_exist_popup()
                if ans == cancel_button.value:  return
                file_path = ''
                continue
            except FileSizeMightBeTooBig:
                ans = file_size_too_big()
                match ans:
                    case 2: ignore_size_limit = True ; file_path = ''
                    case 3: ignore_size_limit = True
                    case 4: return
                continue
            except FileTypeNotAllowed:
                ans = improper_file_type()
                match ans:
                    case 2: ignore_size_limit = True ; file_path = ''
                    case 3: ignore_size_limit = True
                    case 4: return
                continue
            except ImproperDataDefiniton as e:
                ans = preparation_error(e)
                if ans == 2:
                    raw_file = loadFileFromPath(file_path, ignore_size_limit, ignore_file_type)
                    assert type(raw_file) == str
                    self.code_field.setText("".join(raw_file))
                    self.code_field.setHighlight([e.line()], background_color=Qt.GlobalColor.red)
                    self._open_interactive_mode()
                return
            except ImproperJumpMarker as e:
                ans = preprocessing_error()
                if ans == 2:
                    raw_file = loadFileFromPath(file_path, ignore_size_limit, ignore_file_type)
                    assert type(raw_file) == str
                    self.code_field.setText("".join(raw_file))
                    self.code_field.setHighlight([e.line()], background_color=Qt.GlobalColor.red)
                    self._open_interactive_mode()
                return
            except Exception as e:
                unrecognized_error_popup(e)
                return
            break

        self.welcomeScreen.close()
        self.programScreen.show()
        self.variableSection.generate_table()
        self._set_active_state(False)
        self.programScreen.showMaximized()
        self.nextLineButton.setFocus()

    @pyqtSlot()
    def _open_interactive_mode(self):
        self._set_interactive_mode(True)
        self.pagesStack.setCurrentIndex(1)

    @pyqtSlot()
    def _toggle_automatic_execution(self):
        self.automatic_execution = self.startAutoExecButton.isChecked()
    
    @pyqtSlot()
    def _run_next_instruction_or_stop(self):
        if self.program_running and self.startAutoExecButton.isChecked():
            self._executeCommand("next_instruction")
            self.internal_timer.singleShot(self.timer_interval, self._run_next_instruction_or_stop)

    @pyqtSlot()
    def _executeCommand(self, command):
    
        match command:
            case 'start_stop':
                if self.program_running:
                    self._set_active_state(False)
                    self.nextLineButton.setEnabled(False)
                    self.previousLineButton.setEnabled(False)
                    self.startExecutionButton.setText("Uruchom program")
                    self.startExecutionButton.setStyleSheet(f"color: {light_green_color};")
                else:
                    self.nextLineButton.setEnabled(True)
                    self._set_active_state(True)
                    if self.instructionCounter > 0:
                        self.previousLineButton.setEnabled(True)
                    self.startExecutionButton.setText( "Wstrzymaj program")
                    self.startExecutionButton.setStyleSheet(f"color: {darker_yellow};")
                self.program_running = not self.program_running
                if self.startAutoExecButton.isChecked():
                    self.internal_timer.singleShot(self.timer_interval, self._run_next_instruction_or_stop)
            case 'next_instruction':
                response = self.code_handler.executeCommand('next_instruction')
                self.instructionCounter += 1
                self._refresh()
                self._act_on_response(response)
                self.stackSection.refresh_table()
                self.variableSection.refresh_table()
                if self.instructionCounter > 0: self.previousLineButton.setEnabled(True)
            case 'previous_instruction':
                response = self.code_handler.executeCommand('previous_instruction')
                self.instructionCounter -= 1
                self._refresh()
                self._act_on_response(response)
                self.stackSection.refresh_table()
                self.variableSection.refresh_table()
                if self.instructionCounter == 0: self.previousLineButton.setEnabled(False)

    @pyqtSlot()
    def _act_on_response(self, response : dict):
        """
        This funciton is suppose to handle answers from CodeHandler - when we request to
        perform some action with code, CodeHandler, tries to do it using Engine, and 
        returns status of this action - 0 = success ; 1 = defined error ; -1 = undefined error.
        Response is returned in form of dictionary which contains mandatory filed - "status"
        """

        match response['status']:

            #   Everything went as expected - continue execution
            case 0:
                self.code_field.setHighlight(response["highlight"])

            #   Predefined error occured - notify user ; stop execution
            case 1: ...

            #   Undefined error occured - notify user ; stop execution
            case -1: ...

            #   All instructions were executed - notify user about finishing program
            case 'finish':
                self.internal_timer.stop()
                self.code_field.setHighlight([])
                self.nextLineButton.setEnabled(True)
                self.nextLineButton.setDisabled(True)
                self.startExecutionButton.setText("Wstrzymaj program")
                self.startExecutionButton.setStyleSheet(f"color: {darker_yellow};")
                self.program_running = False

            #################    SYSTEM INTERRUP HANDLING    ###################

        if "write_char_to_terminal" in response:
            self.terminal.write_char(response["write_char_to_terminal"])
        if "action_for_terminal" in response:
            self.terminal.perform_action(response["action_for_terminal"])

    @pyqtSlot()
    def _refresh(self):
        for element in self.register_section_elements:
            element.update()
