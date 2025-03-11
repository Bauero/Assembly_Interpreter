"""
This file contains main funciton responsible for handling a gui app
"""
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QPushButton, QFileDialog,
    QComboBox, QCheckBox,QSizePolicy
)
from .custom_gui_elements import *
from .errors import (
    FileDoesntExist, FileSizeMightBeTooBig, FileTypeNotAllowed, ImproperJumpMarker,
    ImproperDataDefiniton
    )
from .helper_functions import loadFileFromPath
from .code_handler import CodeHandler
from .custom_message_boxes import show_custom_popup
from screeninfo import get_monitors

with open('program_code/configs/color_palette.json') as f:  colors = json.load(f)
with open('program_code/configs/names.json') as f:
    all_conumicates = json.load(f)
    supported_languages = all_conumicates["supported_languages"]
    lang_names_each_other = all_conumicates["lang_names_each_other"]
    names = all_conumicates["language_presets"]

alg_cent = Qt.AlignmentFlag.AlignCenter
font_bold_15 = QFont() ; font_bold_15.setBold(True) ; font_bold_15.setPointSize(15)
font_20 = QFont() ; font_20.setPointSize(20)

spacing_10 = 10
min_reg_row_height = 50
max_reg_row_height = 120
max_flags_height = 130

class MainWindow(QWidget):
    """
    This class represents the main window. It stores all information about layout and functions
    which update the app depending on action by the user.
    """

    def __init__(self, code_handler : CodeHandler):
        super().__init__()
        self.code_handler = code_handler
        self.interactive_mode = False
        self.program_running = False
        self.program_finished = False
        self.internal_timer = QTimer()
        self.timer_interval = 1000
        self.internal_timer.setInterval(self.timer_interval)
        self.instructionCounter = 0
        self.language = supported_languages[0]
        self.names_lang = names[self.language]
        self.theme = "dark_mode"
        self._createUserInterface()
        self._set_interactive_mode()
        self.welcomeScreen.show()

    def _createUserInterface(self):
        """This funciton creates whole UI interface"""

        self._createMainMenuPage()
        self._createMainProgramPage()
        self.welcomeScreen.setWindowTitle(self.names_lang["window_title"])
        self.programScreen.setWindowTitle(self.names_lang["window_title"])

        monitor = get_monitors()[0]
        monitor_height, monitor_width = monitor.height, monitor.width
        w_heigth, w_width = monitor_height//4, monitor_width//4
        pos_x = monitor_width//2 - w_width//2
        pos_y = monitor_height//2 - w_heigth//2
        self.welcomeScreen.setGeometry(pos_x, pos_y, w_width, w_heigth)
        self.programScreen.setGeometry(pos_x, pos_y, monitor_width, monitor_height)

    def _createMainMenuPage(self):
        """Defines Main Menu page visible when user lanuches program"""

        self.welcomeScreen = QWidget()
        welcomeLayout = QVBoxLayout()
        welcomeLayout.setAlignment(alg_cent)

        self.welcomeScreenButtons = QWidget()
        welcomeButtonsLayout = QVBoxLayout()
        welcomeButtonsLayout.setAlignment(alg_cent)
        
        self.main_menu_title = QLabel(self.names_lang["main_menu"])
        self.load_file_button = QPushButton(self.names_lang["input_file"])
        self.open_session_button = QPushButton(self.names_lang["interactive"])
        toggle_field_widget = QWidget()
        toggle_language_layout = QHBoxLayout()
        self.toggle_language = QComboBox()
        
        lang_list = []
        for name in lang_names_each_other[self.language]:
            lang_list.append(lang_names_each_other[self.language][name])

        self.toggle_language.addItems(lang_list)
        self.toggle_language.setCurrentIndex(0)
        self.main_menu_title.setFont(font_20)

        self.load_file_button.clicked.connect(self._select_file_to_open_dialog)
        self.open_session_button.clicked.connect(self._open_interactive_mode)
        self.toggle_language.currentIndexChanged.connect(self._lang_change)
        
        welcomeLayout.addWidget(self.main_menu_title, alignment = alg_cent)
        welcomeLayout.addWidget(QLabel(), alignment = alg_cent)
        
        toggle_language_layout.addWidget(QLabel("🌍"))
        toggle_language_layout.addWidget(self.toggle_language, alignment = alg_cent)
        toggle_field_widget.setLayout(toggle_language_layout)
        
        welcomeButtonsLayout.addWidget(self.load_file_button, alignment = alg_cent)
        welcomeButtonsLayout.addWidget(self.open_session_button, alignment = alg_cent)
        welcomeButtonsLayout.addWidget(QLabel(), alignment = alg_cent)
        welcomeButtonsLayout.addWidget(toggle_field_widget, alignment = alg_cent)

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

        HR = self.code_handler.engine.HR
        FR = self.code_handler.engine.FR
        DT = self.code_handler.engine.DS
        EG = self.code_handler.engine
        
        #
        #   Registers Section
        #

        self.registersSection = QWidget()
        registersSectionLayout = QVBoxLayout()
        registersSectionLayout.setAlignment(alg_top)

        self.registers_label = QLabel(self.names_lang["registers"])
        self.registers_label.setFont(font_bold_15)
        registersSectionLayout.addWidget(self.registers_label)

        self.register_section_elements = []
        for mr in ["AX", "BX", "CX", "DX"]:
            self.register_section_elements.append(
                MultipurposeRegister(HR, mr, self.language, self.theme)
            )
        for fr in ["SI", "DI", "SP", "BP", "IP"]:
            self.register_section_elements.append(
                FunctionalRegisters(HR, fr, self.language, self.theme)
            )
        self.register_section_elements.append(Flags(FR, self.language, self.theme))

        for element in self.register_section_elements:
            setattr(self, element.get_name(), element)
            element.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
            element.setMinimumHeight(min_reg_row_height)
            element.setMaximumHeight(max_reg_row_height)
            registersSectionLayout.addWidget(element)

        self.registersSection.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,
                                            QSizePolicy.Policy.Expanding)
        self.register_section_elements[-1].setMinimumHeight(max_flags_height)
        self.registersSection.setLayout(registersSectionLayout)
        registersSectionLayout.setSpacing(no_spacing)

        #
        #   Code and navigation buttons
        #

        self.codeSection = QWidget()
        codeSectionLayout = QFormLayout()
        self.code_label = QLabel(self.names_lang["code"])
        self.code_label.setFont(font_bold_15)
        self.code_field = CodeEditor(self.language, self.theme)
        self.code_field.setMinimumWidth(400)

        self.nextLineButton         = QPushButton(self.names_lang["next_button"])
        self.previousLineButton     = QPushButton(self.names_lang["prev_button"])
        self.saveStateButton        = QPushButton(self.names_lang["save_state"])
        self.startAutoExecCheckbox  = QCheckBox(self.names_lang["auto_button"])
        self.startExecutionButton   = QPushButton(self.names_lang["start_stop_1"])
        
        self.nextLineButton.        setEnabled(self.interactive_mode)
        self.previousLineButton.    setEnabled(self.interactive_mode)
        self.saveStateButton.       setEnabled(self.interactive_mode)
        self.startAutoExecCheckbox. setEnabled(True)

        self.nextLineButton.clicked.        connect(lambda: self._executeCommand('next_instruction'))
        self.previousLineButton.clicked.    connect(lambda: self._executeCommand('previous_instruction'))
        self.startExecutionButton.clicked.  connect(lambda: self._executeCommand('start_stop'))
        self.saveStateButton.clicked.       connect(lambda: self._executeCommand('save_state'))

        self.startExecutionButton.setStyleSheet(
            f'color: {colors[self.theme]["start_stop_button_running"]}')
        self.startAutoExecCheckbox. stateChanged.connect(lambda: self._run_next_instruction_or_stop())
        
        self.comboBoxLabel = QLabel(self.names_lang["interval"])
        self.comboBoxLabel.setAlignment(alg_right)
        self.executionFrequencyList = QComboBox()
        self.executionFrequencyList.addItems(['0.25s', '0.5s', '1s', '2s', '5s'])
        self.executionFrequencyList.setCurrentIndex(2)
        self.executionFrequencyList.currentIndexChanged.connect(self.on_frequency_change)
        
        box = QWidget()
        frequencyBox = QHBoxLayout()
        frequencyBox.addWidget(self.comboBoxLabel)
        frequencyBox.addWidget(self.executionFrequencyList)
        box.setLayout(frequencyBox)

        row_1 = QHBoxLayout()
        row_1.addWidget(self.nextLineButton)
        row_1.addWidget(self.previousLineButton)

        row_2 = QHBoxLayout()
        row_2.addWidget(self.startExecutionButton)
        row_2.addWidget(self.saveStateButton)

        row_3 = QHBoxLayout()
        row_3.addWidget(self.startAutoExecCheckbox)
        row_3.addWidget(box)

        codeSectionLayout.addRow(self.code_label)
        codeSectionLayout.setSpacing(spacing_10)
        codeSectionLayout.addRow(self.code_field)
        codeSectionLayout.addRow(row_1)
        codeSectionLayout.addRow(row_2)
        codeSectionLayout.addRow(row_3)
        self.codeSection.setLayout(codeSectionLayout)

        #
        #   Stack / Segment Section
        #

        self.stackColumn = QVBoxLayout()
        self.segment_label = QLabel(self.names_lang["segment"])
        self.segment_label.setFont(font_bold_15)
        self.stackSection = StackTable(DT, self.language, self.theme)
        self.stackSection.setFixedWidth(200)
        self.stackSection.set_allow_change_content(False)
        self.stackColumn.addWidget(self.segment_label)
        self.stackColumn.addSpacing(spacing_10)
        self.stackColumn.addWidget(self.stackSection)
        
        #
        #   Variable section
        #

        self.variableColumn = QVBoxLayout()
        self.variables_label = QLabel(self.names_lang["variables"])
        self.variables_label.setFont(font_bold_15)
        self.variableSection = VariableTable(EG, self.language, self.theme)
        self.variableColumn.addWidget(self.variables_label)
        self.variableColumn.addSpacing(spacing_10)
        self.variableColumn.addWidget(self.variableSection)

        #
        #   Terminal
        #

        self.terminal_widget = QWidget()
        self.terminal_layout = QVBoxLayout()

        self.terminal_label = QLabel(self.names_lang["terminal"])
        self.terminal_label.setFont(font_bold_15)

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
        programLayout.setSpacing(no_spacing)

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
    def _set_interactive_mode(self):
        for element in self.register_section_elements:
            setattr(self, element.get_name(), element)
            element.set_interactive(self.interactive_mode)

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
                    self, f"{self.names_lang['open_file']}", "${HOME}",
                    "All Files (*);; Python Files (*.py);; PNG Files (*.png)",
                )[0]
                if not file_path: return

            try:
                lines = self.code_handler.readPrepareFile(file_path,
                                                          ignore_size_limit,
                                                          ignore_file_type)
                self.code_field.setText( self.code_handler.gcefat() )
                self.code_field.setHighlight(lines)
                self.code_field.setEditable(False)
            except FileDoesntExist:
                ans = self._show_popup({"popup" : "file_doesnt_exist_popup"})
                if ans == cancel_button.value:  return
                file_path = ''
                continue
            except FileSizeMightBeTooBig:
                ans = self._show_popup({"popup" : "file_size_too_big"})
                match ans:
                    case 2: ignore_size_limit = True ; file_path = ''
                    case 3: ignore_file_type = True
                    case 4: return
                continue
            except FileTypeNotAllowed:
                ans = self._show_popup({"popup" : "improper_file_type"})
                match ans:
                    case 2: ignore_size_limit = True ; file_path = ''
                    case 3: ignore_file_type = True
                    case 4: return
                continue
            except ImproperDataDefiniton as e:
                ans = self._show_popup({"popup" : "data_section_error"})
                if ans == 2:
                    self._load_file_to_interactive(file_path)
                return
            except ImproperJumpMarker as e:
                ans = self._show_popup({"popup" : "improper_label_error"})
                if ans == 2:
                    self._load_file_to_interactive(file_path)
                return
            except Exception as e:
                ans = self._show_popup({"popup" : "unrecognized_error_popup",
                                        "source_error" : e})
                return
            break

        self.welcomeScreen.close()
        self.stackSection.generate_table()
        self.variableSection.generate_table()
        self.programScreen.show()
        self._set_active_state(False)
        self.programScreen.showMaximized()
        self.nextLineButton.setFocus()

    @pyqtSlot()
    def _load_file_to_interactive(self, file_path : str):
        start, raw_file = self.code_handler.load_file_interactive(file_path)
        self.code_field.setText("".join(raw_file))
        self.code_field.setHighlight([start])
        self._open_interactive_mode()

    def _highlight_problematic_line(self, lines : list):
        self.code_field.setHighlight(lines,
                                     colors[self.theme]["error_in_line"])

    @pyqtSlot()
    def _open_interactive_mode(self):
        self.welcomeScreen.close()
        self.stackSection.generate_table()
        self.variableSection.generate_table()
        self.programScreen.showMaximized()
        
        self._set_active_state(False)
        self.interactive_mode = True
        self._set_interactive_mode()
        
        self.code_field.setEnabled(True)
        self.code_field.setFocus()
        self.code_field.setEditable(True)
        self.code_field.setText('')

    @pyqtSlot()
    def _toggle_automatic_execution(self):
        self.automatic_execution = self.startAutoExecCheckbox.isChecked()
    
    @pyqtSlot()
    def _run_next_instruction_or_stop(self):
        if self.program_running and self.startAutoExecCheckbox.isChecked() and \
            not self.program_finished:
            self._executeCommand("next_instruction")
            self.internal_timer.singleShot(self.timer_interval, self._run_next_instruction_or_stop)

    @pyqtSlot()
    def _executeCommand(self, command):
    
        match command:
            case 'start_stop':
                if self.program_running:
                    self._suspend_program()
                else:
                    self._start_program()
                self.program_running = not self.program_running
                if self.startAutoExecCheckbox.isChecked():
                    self.internal_timer.singleShot(self.timer_interval,
                                                   self._run_next_instruction_or_stop)
            case 'next_instruction':
                try:
                    response = self.code_handler.executeCommand('next_instruction')
                    self._act_on_response(response)
                    self.instructionCounter += 1
                    if self.instructionCounter > 0: self.previousLineButton.setEnabled(True)
                except Exception as e: 
                    response = {
                        "status" : 1,
                        "error" : {
                            "popup" : "unrecognized_error_popup",
                            "line" : self.code_handler.get_curr_exec_line(),
                            "param_no" : None,
                            "params" : None,
                            "source_error" : e
                        }
                    }
                    self._act_on_response(response)
            case 'previous_instruction':
                response = self.code_handler.executeCommand('previous_instruction')
                self.instructionCounter -= 1
                if self.instructionCounter == 0: self.previousLineButton.setEnabled(False)
                self._act_on_response(response)

    @pyqtSlot()
    def _act_on_response(self, response : dict):
        """
        This funciton is suppose to handle answers from CodeHandler - when we request to
        perform some action with code, CodeHandler, tries to do it using Engine, and 
        returns status of this action
        -   0 = success
        -   1 = defined error
        -   2 = success, with warnings
        -  -1 = finish execution
        - -12 = finish execution, with warnings
        Response is returned in form of dictionary which contains mandatory filed - "status"
        """

        match response['status']:

            case 0: ...

            case 1:
                self.internal_timer.stop()
                self._set_active_state(False)
                self.nextLineButton.setDisabled(True)
                self.previousLineButton.setEnabled(True)
                self._show_popup(response["error"])
                self.program_running = False
                return

            case 2:
                timer_active = self.internal_timer.isActive()
                if timer_active:    self.internal_timer.stop()
                self._show_popup(response["warning"])
                if timer_active:    self.internal_timer.start()

            case -1:
                self.internal_timer.stop()
                self._refresh()
                self.code_field.setHighlight([])
                self.nextLineButton.setDisabled(True)
                self.startExecutionButton.setText(self.names_lang["start_stop_1"])
                self.startExecutionButton.setStyleSheet(
                    f'color: {colors[self.theme]["start_stop_button_stopped"]};')
                self.program_running = False
                self.program_finished = True
                return
            
            case -12:
                if timer_active:    self.internal_timer.stop()
                self._show_popup(response["warning"])
                self.code_field.setHighlight([])
                self.nextLineButton.setDisabled(True)
                self.startExecutionButton.setText(self.names_lang["start_stop_1"])
                self.startExecutionButton.setStyleSheet(
                    f'color: {colors[self.theme]["start_stop_button_stopped"]};')
                self.program_running = False
                self.code_field.setHighlight([])
                if timer_active:    self.internal_timer.start()
                return

        terminal_operation = response.get("terminal", None)
        if terminal_operation:
            self._perform_terminal_aciton(terminal_operation)
        self.code_field.setHighlight(response["highlight"])
        self._refresh()

    @pyqtSlot()
    def _perform_terminal_aciton(self, action : str):
        """This method performs aciton requireing user interaction with terminal"""
        
        ...

    @pyqtSlot()
    def _show_popup(self, dialog : dict):
        """This method request showing popup for the current language and message"""
        
        return show_custom_popup(self.language, dialog)

    @pyqtSlot()
    def _refresh(self):
        """This method refreshes elemetns in the main program"""

        for element in self.register_section_elements:
            element.update()    
        self.stackSection.refresh_table()
        self.variableSection.refresh_table()

    @pyqtSlot()
    def _start_program(self):
        if not self.program_finished:
            self.nextLineButton.setEnabled(True)
        self._set_active_state(True)
        if self.instructionCounter > 0:
            self.previousLineButton.setEnabled(True)
        self.startExecutionButton.setText(self.names_lang["start_stop_2"])
        self.startExecutionButton.setStyleSheet(
            f'color: {colors[self.theme]["start_stop_button_stopped"]};')

        if self.interactive_mode:
            self.code_field.setEditable(False)
            new_lines = self.code_handler.startInteractive(self.code_field.toPlainText())
            self.code_field.setHighlight(new_lines)
            if new_lines:
                self.instructionCounter = 0
                self.code_handler.engine.reset()
                self._refresh()

    @pyqtSlot()
    def _suspend_program(self):
        self._set_active_state(False)
        self.nextLineButton.setDisabled(True)
        self.previousLineButton.setEnabled(False)
        self.startExecutionButton.setText(self.names_lang["start_stop_1"])
        self.startExecutionButton.setStyleSheet(
            f'color: {colors[self.theme]["start_stop_button_running"]};')
        
        if self.interactive_mode:
            self.code_field.setDisabled(False)
            self.code_field.setEditable(True)

    @pyqtSlot()
    def _lang_change(self):
        """This method is repsonsible for reloading elements in GUI to show
        test in selected language"""
        
        option = self.toggle_language.currentIndex()
        lang_before = self.language
        
        self.language = supported_languages[option]
        self.names_lang = names[self.language]
        
        if lang_before != self.language:
            
            # Program Title
            self.welcomeScreen.setWindowTitle(self.names_lang["window_title"])
            self.programScreen.setWindowTitle(self.names_lang["window_title"])

            # Welcome Screen
            self.main_menu_title.setText(self.names_lang["main_menu"])
            self.load_file_button.setText(self.names_lang["input_file"])
            self.open_session_button.setText(self.names_lang["interactive"])
            
            # Welcome Screen - Toggle Language
            self.toggle_language.blockSignals(True)
            self.toggle_language.clear()
            lang_list = []
            for name in lang_names_each_other[self.language]:
                lang_list.append(lang_names_each_other[self.language][name])
            self.toggle_language.addItems(lang_list)
            self.toggle_language.setCurrentIndex(option)
            self.toggle_language.blockSignals(False)
            self.load_file_button.setFocus()
            
            # Program - Section Names
            self.registers_label.setText(self.names_lang["registers"])
            self.code_label.setText(self.names_lang["code"])
            self.segment_label.setText(self.names_lang['segment'])
            self.variables_label.setText(self.names_lang['variables'])
            self.terminal_label.setText(self.names_lang["terminal"])

            # Program - Control buttons
            self.nextLineButton.setText(self.names_lang['next_button'])
            self.previousLineButton.setText(self.names_lang['prev_button'])
            self.startAutoExecCheckbox.setText(self.names_lang['auto_button'])
            self.startExecutionButton.setText(self.names_lang['start_stop_1'])
            self.saveStateButton.setText(self.names_lang["save_state"])
            self.comboBoxLabel.setText(self.names_lang['interval'])
            
            # Program - Names in tables and register hints
            self.stackSection.set_header(self.language)
            self.variableSection.set_header(self.language)
            for e in self.register_section_elements:
                e.set_hint(self.language)
