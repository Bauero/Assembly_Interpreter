"""
This file containst gustom GUI structures which are then later used in main gui
file
"""

from .engine import Engine
from .hardware_memory import DataSegment
from .flag_register import FlagRegister
from .helper_functions import return_name_from_size
from PyQt6.QtCore import Qt, QRect, QTimer, pyqtSignal
from PyQt6.QtGui import (
    QFont, QTextCursor, QPainter, QColor, QTextFormat, QKeySequence, QPalette,
    QKeyEvent)
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QHBoxLayout, QLineEdit, QTextEdit,
    QMessageBox, QPlainTextEdit, QTableWidget, QHeaderView, QTableWidgetItem, 
    QAbstractItemView,QApplication)
import json

with open('program/names.json') as f:
    names = json.load(f)["language_specific_names"]

alg_cent =      Qt.AlignmentFlag.AlignCenter
alg_right =     Qt.AlignmentFlag.AlignRight
alg_top =       Qt.AlignmentFlag.AlignTop
alg_jst =       Qt.AlignmentFlag.AlignJustify
ok_button =     QMessageBox.StandardButton.Ok
cancel_button = QMessageBox.StandardButton.Cancel

def color_txt(color : str, text : str, font_size_px : int = 14) -> str:
    return f'<pre><span style="font-size: {font_size_px}px; color: {color};">{text}</span></pre>'

class MultipurposeRegister(QWidget):
    """This class creates a widget for displaying multipurpose register, splited into
    high and low bits as well as a dedicated field for displaying decimal value of register
    """

    def __init__(self, HR, register_name, text_color = 'white', custom_name = ''):
        super().__init__()

        self.register_name = register_name
        self.HR = HR
        
        # Main horizontal layout for the row
        row_layout = QHBoxLayout()
        
        # Register name label (e.g., EAX)
        self.register_label = QLabel(register_name)
        self.register_label.setStyleSheet(f"color: {text_color};")
        font = QFont() ; font.setBold(True) ; font.setPointSize(16)
        self.register_label.setFont(font)
        row_layout.addWidget(self.register_label)
        self.register_label.setToolTip(color_txt('#8F8F8F', custom_name))
        row_layout.insertSpacing(1,9)
        
        # Container for the H and L labels and main text fields
        main_field_layout = QVBoxLayout()

        # Main text fields in a horizontal layout with no spacing
        text_field_layout = QHBoxLayout()
        text_field_layout.setSpacing(0)  # No gaps between fields

        self.register_high_bits = QLineEdit()
        self.register_high_bits.setStyleSheet("QLineEdit { letter-spacing: 1px; }")
        self.register_high_bits.setInputMask("BBBBBBBB")  # 8-bitowa wartość binarna
        self.register_high_bits.setFixedWidth(90)  # Adjust for 8 characters
        self.register_high_bits.setFixedHeight(20)  # Adjust for 8 characters
        self.register_high_bits.setReadOnly(True)
        self.register_high_bits.setAlignment(alg_cent)
        text_field_layout.addWidget(self.register_high_bits)

        self.register_low_bits = QLineEdit()
        self.register_low_bits.setStyleSheet("QLineEdit { letter-spacing: 1px; }")
        self.register_low_bits.setInputMask("BBBBBBBB")  # 8-bitowa wartość binarna
        self.register_low_bits.setFixedWidth(90)  # Adjust for 8 characters
        self.register_low_bits.setFixedHeight(20)  # Adjust for 8 characters
        self.register_low_bits.setReadOnly(True)
        self.register_low_bits.setAlignment(alg_cent)
        text_field_layout.addWidget(self.register_low_bits)

        main_field_layout.addLayout(text_field_layout)

        # Add main_field_layout to the row layout
        row_layout.addLayout(main_field_layout)

        # Equals label
        equals_label = QLabel("=")
        equals_label.setFixedHeight(20)
        row_layout.addWidget(equals_label)

        # Smaller text field (8 characters wide)
        self.register_decimal_value = QLineEdit()
        self.register_decimal_value.setFixedWidth(60)  # Adjust width as needed
        self.register_decimal_value.setFixedHeight(20)  # Adjust width as needed
        self.register_decimal_value.setReadOnly(True)
        self.register_decimal_value.setAlignment(alg_cent)
        row_layout.addWidget(self.register_decimal_value)
        
        # Set the layout for this widget
        self.setLayout(row_layout)
        self.update()

    def _setRegisterValue(self, value : int | list | str):
        """This method sets value as bits in register"""
        
        if type(value) == list:                  # Put this value for 32 bit mode
            if len(value) < 16:                             # 32
                while len(value) < 16:                      # 32
                    value.insert(0,0)
            if len(value) > 16:                             # 32
                value = value[-16:]                         # -32
            value = "".join((str(x) for x in value))

        elif type(value) == int:
            if value >= 2**16 or value <= -(2**8):         # 2**32 | 2**16
                value %= 2**16+1                           # 2**32 + 1
            value = bin(value)[2:]
        
        assert type(value) == str
        value = value.zfill(16)                            # 32

        # self.register_upper_bits.setText(value[-32:-16]) # Uncomment this line 
        self.register_high_bits.setText(value[-16:-8])
        self.register_low_bits.setText(value[-8:])
        self.register_decimal_value.setText(f"{int(value, base=2)}")

    def update(self):
        self._setRegisterValue(self.HR.readFromRegister(self.register_name))

    def get_name(self):
        return self.register_name
    
    def set_interactive(self, value : bool = False):
        # self.register_upper_bits.setReadOnly(not value) # uncomment this line for 32
        self.register_high_bits.setReadOnly(not value)
        self.register_low_bits.setReadOnly(not value)
        self.register_decimal_value.setReadOnly(not value)

    def set_hint(self, text : str) -> None:
        self.register_label.setToolTip(color_txt('#8F8F8F', text))


class FunctionalRegisters(QWidget):
    def __init__(self, HR, register_name, text_color = 'white', custom_name = ''):
        super().__init__()

        self.register_name = register_name
        self.HR = HR

        row_layout = QHBoxLayout()

        self.register_label = QLabel(register_name)
        self.register_label.setFixedWidth(30)
        self.register_label.setStyleSheet(f"color: {text_color};")
        font = QFont() ; font.setBold(True) ; font.setPointSize(16)
        self.register_label.setFont(font)
        row_layout.addWidget(self.register_label)
        self.register_label.setToolTip(color_txt('#8F8F8F', custom_name))

        self.register_content = QLineEdit()
        self.register_content.setStyleSheet("QLineEdit { letter-spacing: 1px; }")
        self.register_content.setFixedWidth(180)
        self.register_content.setFixedHeight(20)
        self.register_content.setReadOnly(True)
        self.register_content.setAlignment(alg_cent)
        row_layout.addWidget(self.register_content)

        # Equals label
        equals_label = QLabel("=")
        row_layout.addWidget(equals_label)

        # Smaller text field (8 characters wide)
        self.register_decimal_value = QLineEdit()
        self.register_decimal_value.setFixedWidth(60)  # Adjust width as needed
        self.register_decimal_value.setFixedHeight(20)  # Adjust width as needed
        self.register_decimal_value.setReadOnly(True)
        self.register_decimal_value.setAlignment(alg_cent)
        row_layout.addWidget(self.register_decimal_value)

        self.setLayout(row_layout)
        self.update()

    def _setRegisterValue(self, value : int | list | str):
        """This method sets value as bits in register"""
        
        if type(value) == list:                  # Put this value for 32 bit mode
            if len(value) < 16:                             # 32
                while len(value) < 16:                      # 32
                    value.insert(0,0)
            if len(value) > 16:                             # 32
                value = value[-16:]                         # -32
            value = "".join((str(x) for x in value))

        elif type(value) == int:
            if value >= 2**16 or value <= -(2**8):         # 2**32 | 2**16
                value %= 2**16+1                           # 2**32 + 1
            value = bin(value)[2:]
        
        assert type(value) == str
        value = value.zfill(16)                            # 32

        self.register_content.setText(value)
        self.register_decimal_value.setText(f"{int(value, base=2)}")

    # Methods dedicated for interactive mode

    def update(self):
        self._setRegisterValue(self.HR.readFromRegister(self.register_name))

    def get_name(self):
        return self.register_name

    def set_interactive(self, value : bool = False):
        self.register_content.setReadOnly(not value)

    def set_hint(self, text : str) -> None:
        self.register_label.setToolTip(color_txt('#8F8F8F', text))


class Flags(QWidget):
    """
    This class is responsible for display of flag register = it containts a text
    field with source value, and below it, there are checkbox'es working like 
    indicators for all flags which are important for the user
    """

    def __init__(self, FR : FlagRegister, language : str):
        super().__init__()
        self.FR = FR
        wrapper = QHBoxLayout()
        body = QFormLayout()
        firts_row = QHBoxLayout()
        register_label = QLabel(color_txt('#30BB73', names[language]["flags"], 16))
        font = QFont() ; font.setBold(True) #; font.setPointSize(16)
        register_label.setFont(font)
        firts_row.addWidget(register_label)
        firts_row.insertSpacing(1,20)

        self.register_content = QLineEdit()
        self.register_content.setStyleSheet("QLineEdit { letter-spacing: 1px; }")
        self.register_content.setFixedWidth(200)
        self.register_content.setReadOnly(True)
        self.register_content.setAlignment(alg_cent)
        self.register_content.returnPressed.connect(self._validate_register_content)
        firts_row.addWidget(self.register_content)

        self.flag_indicators_row_1 = QHBoxLayout()
        self.flag_indicators_row_2 = QHBoxLayout()
        self.flag_indicators_row_3 = QHBoxLayout()

        flags = ['Overflow', 'Direction', 'Interrupt',
                    'Trap', 'Sign', 'Zero',
                    'Auxiliary carry', 'Parity', 'Carry']

        for f in flags:
            attr_name = f"{f.lower().replace(' ', '_')}_flag"
            setattr(self, attr_name, CustomIndicator(f))
            obj = getattr(self, attr_name)
            obj.setToolTip(color_txt('#8F8F8F', names[language][attr_name]))
            obj.stateChanged.connect(lambda _, flag=f: self._flag_indicator_clicked(flag))

        self.flag_indicators_row_1.addWidget(self.overflow_flag)
        self.flag_indicators_row_1.insertSpacing(1,32)
        self.flag_indicators_row_1.addWidget(self.direction_flag)
        self.flag_indicators_row_1.insertSpacing(3,21)
        self.flag_indicators_row_1.addWidget(self.interrupt_flag)

        self.flag_indicators_row_2.addWidget(self.trap_flag)
        self.flag_indicators_row_2.insertSpacing(1,34)
        self.flag_indicators_row_2.addWidget(self.sign_flag)
        self.flag_indicators_row_2.insertSpacing(3,22)
        self.flag_indicators_row_2.addWidget(self.zero_flag)

        self.flag_indicators_row_3.addWidget(self.auxiliary_carry_flag)
        self.flag_indicators_row_3.insertSpacing(1,1)
        self.flag_indicators_row_3.addWidget(self.parity_flag)
        self.flag_indicators_row_3.insertSpacing(3,22)
        self.flag_indicators_row_3.addWidget(self.carry_flag)

        body.addRow(firts_row)
        body.addRow(self.flag_indicators_row_1)
        body.addRow(self.flag_indicators_row_2)
        body.addRow(self.flag_indicators_row_3)

        wrapper.addLayout(body)
        self.setLayout(wrapper)
        self.update()

    def _flag_indicator_clicked(self, flag_name : str):
        flag_position = None

        match flag_name:
            case 'Overflow':            flag_position = -12
            case 'Direction':           flag_position = -11
            case 'Interrrupt':          flag_position = -10
            case 'Trap':                flag_position = -9
            case 'Sign':                flag_position = -8
            case 'Zero':                flag_position = -7
            case 'Auxiliary carry':     flag_position = -5
            case 'Parity':              flag_position = -3
            case 'Carry':               flag_position = -1
        
        value = self.register_content.text()[flag_position]
        new_value = "0" if value == "1" else "1"
        content = list(self.register_content.text())
        content[flag_position] = new_value
        self.FR.setFlagRaw(content)
        self.register_content.setText("".join(content))

    def _setRegisterValue(self, value : int | list | str):
        """This method sets value as bits in register"""
        
        if type(value) == list:                  # Put this value for 32 bit mode
            if len(value) < 16:                             # 32
                while len(value) < 16:                      # 32
                    value.insert(0,0)
            if len(value) > 16:                             # 32
                value = value[-16:]                         # -32
            value = "".join((str(x) for x in value))

        elif type(value) == int:
            if value >= 2**16 or value <= -(2**8):         # 2**32 | 2**16
                value %= 2**16+1                           # 2**32 + 1
            value = bin(value)[2:]
        
        assert type(value) == str
        value = value.zfill(16)                            # 32

        self.register_content.setText(value)

        self.overflow_flag.         setChecked(value[-12] == "1")
        self.direction_flag.        setChecked(value[-11] == "1")
        self.interrupt_flag.        setChecked(value[-10] == "1")
        self.trap_flag.             setChecked(value[-9] == "1")
        self.sign_flag.             setChecked(value[-8] == "1")
        self.zero_flag.             setChecked(value[-7] == "1")
        self.auxiliary_carry_flag.  setChecked(value[-5] == "1")
        self.parity_flag.           setChecked(value[-3] == "1")
        self.carry_flag.            setChecked(value[-1] == "1")
   
    def update(self):
        self._setRegisterValue(self.FR.readFlags())

    def get_name(self):
        return "FLAGS"
    
    def set_interactive(self, value : bool = False):
        for attr_name in dir(self):
            if attr_name.endswith('_flag'):
                attr_value = getattr(self, attr_name)
                attr_value.setModifiable(value)
        self.register_content.setReadOnly(not value)

    def _validate_register_content(self):
        text = self.register_content.text()
        if not set(text).issubset(('1','0')):
            self.showErrorMessage("Improper value", "Only text containing 1's and 0's can be put in this field!")
        adjusted_text =text.zfill(16)[-16:]
        self._setRegisterValue(adjusted_text)

    def showErrorMessage(self, title : str, message : str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec()

    def set_hint(self, language : str) -> None:
        self.overflow_flag.         setToolTip(color_txt('#8F8F8F', names[language]["overflow_flag"]))
        self.direction_flag.        setToolTip(color_txt('#8F8F8F', names[language]["direction_flag"]))
        self.interrupt_flag.        setToolTip(color_txt('#8F8F8F', names[language]["interrupt_flag"]))
        self.trap_flag.             setToolTip(color_txt('#8F8F8F', names[language]["trap_flag"]))
        self.sign_flag.             setToolTip(color_txt('#8F8F8F', names[language]["sign_flag"]))
        self.zero_flag.             setToolTip(color_txt('#8F8F8F', names[language]["zero_flag"]))
        self.auxiliary_carry_flag.  setToolTip(color_txt('#8F8F8F', names[language]["auxiliary_carry_flag"]))
        self.parity_flag.           setToolTip(color_txt('#8F8F8F', names[language]["parity_flag"]))
        self.carry_flag.            setToolTip(color_txt('#8F8F8F', names[language]["carry_flag"]))


class LimitedInputTextEdit(QTextEdit):
    inputFinished = pyqtSignal(str)  # Signal emitted when input is done

    def __init__(self, char_limit = 1000):
        super().__init__()
        self.char_limit = char_limit  # Limit of characters
        self.current_input = ""       # Stores current input
        self.setUndoRedoEnabled(False)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        
        # Handle Enter key
        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            self.append("")  # Move to next line
            self.inputFinished.emit(self.current_input)
            self.current_input = ""
            return

        # Handle Backspace
        elif key == Qt.Key.Key_Backspace:
            if len(self.current_input) > 0:
                self.current_input = self.current_input[:-1]
                self.textCursor().deletePreviousChar()
            return

        # Limit input to char_limit
        elif event.text() and len(self.current_input) < self.char_limit:
            self.current_input += event.text()
            self.insertPlainText(event.text())
        else:
            # Ignore other keys or excess input
            pass

    def reset_char_limit(self):     self.char_limit = 1000


class LimitedInputTextEdit(QTextEdit):
    inputFinished = pyqtSignal(str)

    def __init__(self, char_limit=20):
        super().__init__()
        self.char_limit = char_limit
        self.current_input = ""
        self.setUndoRedoEnabled(False)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            self.append("")
            self.inputFinished.emit(self.current_input)
            self.current_input = ""
            return

        elif key == Qt.Key.Key_Backspace:
            if len(self.current_input) > 0:
                self.current_input = self.current_input[:-1]
                self.textCursor().deletePreviousChar()
            return

        elif event.text() and len(self.current_input) < self.char_limit:
            self.current_input += event.text()
            self.insertPlainText(event.text())


class Terminal(QWidget):
    def __init__(self):
        super().__init__()

        # Layout for Terminal
        layout = QVBoxLayout()

        # Custom LimitedInputTextEdit
        self.terminal = LimitedInputTextEdit(20)  # Limit to 20 chars
        font = QFont()
        font.setPointSize(15)
        self.terminal.setFont(font)
        self.terminal.setMinimumHeight(100)

        # Connect signal
        self.terminal.inputFinished.connect(self.handle_input)

        # Add widgets to layout
        layout.addWidget(self.terminal)
        self.setLayout(layout)

    def handle_input(self, user_input: str):
        """Handle input when user presses Enter."""
        print(f"User input: {user_input}")  # You can process/store input here

    def write_char(self, char: int):
        """Write characters to terminal programmatically."""
        text = self.terminal.toPlainText()
        self.terminal.setPlainText(text + chr(char))


class CustomIndicator(QLabel):
    # Signal to notify FlagRegister on toggle (emits new state: True/False)
    stateChanged = pyqtSignal(bool)

    def __init__(self, text, *args):
        super().__init__(text)
        self.labelText = text
        self.turnedOnState = False
        self.modifiable = True
        self.setOff()
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def setOn(self):
        self.setText(f"🟩 {self.labelText}")
        self.turnedOnState = True

    def setOff(self):
        self.setText(f"🟥 {self.labelText}")
        self.turnedOnState = False

    def toggleState(self):
        if self.turnedOnState:
            self.setOff()
        else:
            self.setOn()
        # Emit signal with new state
        self.stateChanged.emit(self.turnedOnState)

    def setChecked(self, state):
        if bool(state):
            self.setOn()
        else:
            self.setOff()

    def setModifiable(self, option):
        self.modifiable = bool(option)

    def mousePressEvent(self, event):
        if self.modifiable and event.button() == Qt.MouseButton.LeftButton:
            self.toggleState()
        super().mousePressEvent(event)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.myeditor = editor

    def sizeHint(self):
        return self.myeditor.line_number_area_width(), 0

    def paintEvent(self, event):
        self.myeditor._lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    """This class is responsible for creation of code field, which allows for display of 
    custom text field, with numered lines, and option to highlight a certain line"""

    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)

        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)  # Wyłącz zawijanie linii
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Pasek poziomy pojawi się w razie potrzeby

        self.blockCountChanged.connect(self.updateLine_number_area_width)
        self.updateRequest.connect(self.updateLineNumberArea)

        self.updateLine_number_area_width(0)
        self.textCursor().movePosition(QTextCursor.MoveOperation.Start)

        self.highlighted_lines = []

    def line_number_area_width(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count //= 10
            digits += 1
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLine_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy != 0:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLine_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def _lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = " " + str(blockNumber + 1) + "  "
                # painter.setPen(Qt.GlobalColor.black)
                painter.drawText(0, int(top), self.lineNumberArea.width(), height, Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def setHighlight(self, line_numbers, 
                 background_color=Qt.GlobalColor.blue, 
                 text_color=Qt.GlobalColor.white):
        """
        Podświetla wybrane linie i przewija widok, aby podświetlona linia była na ekranie.

        Args:
            line_numbers (list[int]): Lista numerów linii do podświetlenia (1-based).
            background_color (QColor): Kolor tła dla podświetlenia.
            text_color (QColor): Kolor tekstu w podświetlonych liniach.
        """
        extraSelections = []

        for line_number in line_numbers:
            if line_number <= 0:
                continue

            cursor = QTextCursor(self.document().findBlockByLineNumber(line_number - 1))
            if not cursor.isNull():
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(QColor(background_color))
                selection.format.setForeground(QColor(text_color))
                selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
                selection.cursor = cursor
                selection.cursor.clearSelection()

                extraSelections.append(selection)

        self.highlighted_lines = line_numbers
        self.setExtraSelections(extraSelections)

        # PRZEWIJANIE DO PODŚWIETLONEJ LINII
        if line_numbers:
            target_line = line_numbers[0]  # Wybieramy pierwszą podświetloną linię
            block = self.document().findBlockByLineNumber(target_line - 1)
            if block.isValid():
                cursor = QTextCursor(block)
                self.setTextCursor(cursor)  # Ustawiamy kursor na podświetloną linię
                self.ensureCursorVisible()  # Upewniamy się, że linia jest widoczna

                # Alternatywnie, możemy przewijać ręcznie
                scroll_bar = self.verticalScrollBar()
                scroll_position = line_number - 20 #int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top() - (self.viewport().height() // 2))
                scroll_bar.setValue(scroll_position)

            # Przechowujemy informacje o podświetlonych liniach
            self.highlighted_lines = line_numbers

            # Aktualizacja podświetleń w edytorze
            self.setExtraSelections(extraSelections)

    def setText(self, text):
        self.setPlainText(text)

    def setEditable(self, editable):
        self.setReadOnly(not editable)


class StackTable(QTableWidget):
    """This class allows to display Stack as a table with option to easily change
    content"""
    def __init__(self, data: DataSegment):
        super().__init__()
        self.no_of_rows = 65536
        self.data = data
        self.data_copy = None
        self.font = QFont()
        self.font.setBold(True)
        self.font.setPointSize(15)
        self.font.setItalic(True)

        # Initialize table properties
        self.setRowCount(self.no_of_rows)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Adr.", "Licz. Bin.", "Dec."])
        self.setColumnWidth(2,1)
        # self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)

        # Hide row numbers
        self.verticalHeader().setVisible(False)

        # Set grid visibility
        self.setShowGrid(True)
        self.setGridStyle(Qt.PenStyle.SolidLine)
        self.setStyleSheet("QTableWidget {gridline-color: #606060; \
                           letter-spacing: 1px; font-size: 13px}")

        # Enable editability
        self.cellChanged.connect(self.onCellChanged)

    def set_allow_change_content(self, allow = True):
        self.allow_change = allow
        if allow:
            self.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        else:
            self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def generate_table(self):
        """Refresh table contents"""
        fresh_data = self.data.data
        self.data_copy = fresh_data[:]

        self.cellChanged.disconnect()

        for row, address in enumerate(range(self.no_of_rows-1, -1, -1)):
            address_hex = hex(address)[2:].upper()
            value_int = self.data_copy[address]
            value_bin = bin(value_int)[2:].zfill(8)
            
            row_no = QTableWidgetItem(address_hex)
            row_no.setFont(self.font)

            self.setItem(row, 0, row_no)
            self.setItem(row, 1, QTableWidgetItem(value_bin))
            self.setItem(row, 2, QTableWidgetItem(str(value_int)))
        
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.cellChanged.connect(self.onCellChanged)

    def refresh_table(self):
        fresh_data = self.data.data
        self.cellChanged.disconnect()

        if self.data_copy != fresh_data:
            for row, address in enumerate(range(self.no_of_rows-1, -1, -1)):
                if self.data_copy[address] != fresh_data[address]:
                    value_int = fresh_data[address]
                    value_bin = bin(value_int)[2:].zfill(8)
                    self.setItem(row, 1, QTableWidgetItem(value_bin))
                    self.setItem(row, 2, QTableWidgetItem(str(value_int)))
                    self.data_copy[address] = fresh_data[address]
                    self.highlightChange(row, 1, QColor(255, 255, 0, 83))
                    self.highlightChange(row, 2, QColor(255, 255, 0, 83))

        self.cellChanged.connect(self.onCellChanged)

    def onCellChanged(self, row, column):
        """Handle cell edits and enforce binary/decimal rules"""

        self.blockSignals(True)
        item = self.item(row, column)
        value = item.text().strip()
        
        if not self.allow_change or not value:
            self.restorePreviousValue(row)
            self.blockSignals(False)
            return

        match column:
            case 0:
                self.showErrorMessage("Operation forbidden!",
                    "It's not possible to edit memory address!")
                self.restorePreviousValue(row)
                self.blockSignals(False)
            case 1:
                if not all(c in '01' for c in value):
                    self.showErrorMessage("Invalid binary number",
                        "Enter valid binary number - only 1's and 0's")
                    self.restorePreviousValue(row)
                else:
                    decimal_value = int(value, 2)
                    if decimal_value > 255:
                        self.showErrorMessage("Incorrect value",
                            "Value too big - value have to be between 0 and 255")
                        self.restorePreviousValue(row)
                        return
                    self.setItem(row, 1, QTableWidgetItem(value.zfill(8)))
                    self.setItem(row, 2, QTableWidgetItem(str(decimal_value)))
                    self.highlightChange(row, 1)
                    self.highlightChange(row, 2)
            case 2:
                if not value.isdigit():
                    self.showErrorMessage("Incorrect decimal value",
                        "Enter valid decimal value!")
                    self.restorePreviousValue(row)
                else:
                    decimal_value = int(value)
                    if decimal_value > 255 or decimal_value < 0:
                        self.showErrorMessage("Incorrect value",
                            "Value too big - value have to be between 0 and 255")
                        self.restorePreviousValue(row)
                        return
                    binary_value = bin(decimal_value)[2:].zfill(8)
                    self.setItem(row, 1, QTableWidgetItem(binary_value))
                    self.highlightChange(row, 1)
                    self.highlightChange(row, 2)

        self.blockSignals(False)  # Re-enable signals

    def showErrorMessage(self, title : str, message : str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec()

    def restorePreviousValue(self, row):
        """Restore the original value before it was edited"""
        value_int = self.data_copy[self.no_of_rows - row]
        value_bin = bin(value_int)[2:].zfill(8)

        address = hex(self.no_of_rows - 1 - row)[2:].upper()
        row_no = QTableWidgetItem(address)
        row_no.setFont(self.font)

        self.setItem(row, 0, row_no)
        self.setItem(row, 1, QTableWidgetItem(str(value_bin)))
        self.setItem(row, 2, QTableWidgetItem(str(value_int)))

    def copySelectionToClipboard(self):
        selected_ranges = self.selectedRanges()
        if not selected_ranges:
            return

        copied_text = []
        
        for selection in selected_ranges:
            rows = []
            for row in range(selection.topRow(), selection.bottomRow() + 1):
                cols = []
                for col in range(selection.leftColumn(), selection.rightColumn() + 1):
                    item = self.item(row, col)
                    cols.append(item.text() if item else "")  # Get text or empty string if None
                rows.append("\t".join(cols))  # Separate columns by tab (Excel format)
            copied_text.append("\n".join(rows))  # Separate rows by new line

        clipboard = QApplication.clipboard()
        clipboard.setText("\n".join(copied_text))  # Copy formatted text to clipboard

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copySelectionToClipboard()
        else:
            super().keyPressEvent(event)

    def highlightChange(self, row, column, color):
        item = self.item(row, column)
        if not item:
            return

        # Get the original background color (handles dark/light mode properly)
        default_color = self.palette().color(QPalette.ColorRole.Base)
        
        # If item already has a custom background, use it
        original_color = item.background().color()
        if not original_color.isValid() or original_color == QColor(0, 0, 0):  
            original_color = default_color  

        item.setBackground(color)
        QTimer.singleShot(500, lambda: self.resetCellColor(row, column, original_color))

    def resetCellColor(self, row, column, color):
        self.blockSignals(True)
        item = self.item(row, column)
        if item:
            item.setBackground(color)
        self.blockSignals(False)


class VariableTable(QTableWidget):
    """This class allows to display Stack as a table with option to easily change
    content"""
    def __init__(self, engine : Engine):
        super().__init__()
        self.data = engine.data
        self.data_copy = []
        self.engine = engine
        self.allow_change = False
        self.font = QFont()
        self.font.setBold(True)
        self.font.setPointSize(15)
        self.font.setItalic(True)

        # Initialize table properties
        columns = ["Name","Addr.", "Size", "Format", "Content"]
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

        # Hide row numbers
        self.verticalHeader().setVisible(False)

        # Set grid visibility
        self.setShowGrid(True)
        self.setGridStyle(Qt.PenStyle.SolidLine)
        self.setStyleSheet("QTableWidget {gridline-color: #606060;}")

        # Enable editability
        self.cellChanged.connect(self.onCellChanged)

    def set_allow_change_content(self, allow = True):
        self.allow_change = allow
        if allow:
            self.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        else:
            self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def generate_table(self):
        """Refresh table contents"""

        self.cellChanged.disconnect()
        self.variables = self.engine.variables
        self.setRowCount(len(self.variables))

        for row, var in enumerate(self.variables):
            variable = self.variables[var]
            address = variable['address']
            size = variable['size']
            format_str = return_name_from_size(variable['format'])
            content = self.data.get_data(address, size)
            binary_content = " ".join([bin(c)[2:].zfill(8) for c in content])

            var_name = QTableWidgetItem(var)
            var_name.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            item_address = QTableWidgetItem(str(address))
            item_address.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            item_size = QTableWidgetItem(str(size))
            item_size.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            item_format =  QTableWidgetItem(format_str)
            item_format.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            self.setItem(row, 0, var_name)
            self.setItem(row, 1, item_address)
            self.setItem(row, 2, item_size)
            self.setItem(row, 3, item_format)
            self.setItem(row, 4, QTableWidgetItem(binary_content))

            self.data_copy.append(content)
        
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.cellChanged.connect(self.onCellChanged)

    def refresh_table(self):
        
        self.cellChanged.disconnect()

        for row, var in enumerate(self.variables):
            variable = self.variables[var]
            address = variable['address']
            size = variable['size']
            content = self.data.get_data(address, size)

            if self.data_copy[row] != content:
                binary_content = " ".join([bin(c)[2:].zfill(8) for c in content])
                self.setItem(row, 4, QTableWidgetItem(binary_content))
                self.highlightChange(row, 4, QColor(255, 255, 0, 83))
                self.data_copy[row] = content

        self.cellChanged.connect(self.onCellChanged)

    def onCellChanged(self, row, column):
        """Handle cell edits and enforce binary/decimal rules"""

        self.blockSignals(True)
        item = self.item(row, column)
        value = item.text().strip()
        
        if not self.allow_change or not value:
            self.restorePreviousValue(row)
            self.blockSignals(False)
            return

        match column:
            case 0:
                self.showErrorMessage("Operation forbidden!",
                    "It's not possible to edit variable name!")
                self.restorePreviousValue(row)
                self.blockSignals(False)
            case 1:
                self.showErrorMessage("Operation forbidden!",
                    "It's not possible to edit variable address!")
                self.restorePreviousValue(row)
                self.blockSignals(False)
            case 2:
                self.showErrorMessage("Operation forbidden!",
                    "It's not possible to edit variable size!")
                self.restorePreviousValue(row)
                self.blockSignals(False)
            case 3:
                self.showErrorMessage("Operation forbidden!",
                    "It's not possible to edit variable format!")
                self.restorePreviousValue(row)
                self.blockSignals(False)
            case 4:
                if not all(c in '01' for c in value):
                    self.showErrorMessage("Invalid binary number",
                        "Enter valid binary number - only 1's and 0's")
                    self.restorePreviousValue(row)
                else:
                    length = (len(value)//8 + 1) * 8 if len(value)//8 < len(value)/8 else len(value)//8
                    self.setItem(row, 4, QTableWidgetItem(value.zfill(length)))
                    self.highlightChange(row, 4)

        self.blockSignals(False)  # Re-enable signals

    def showErrorMessage(self, title : str, message : str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec()

    def restorePreviousValue(self, row):
        """Restore the original value before it was edited"""
        content = self.data_copy[row]
        binary_content = " ".join([bin(c)[2:].zfill(8) for c in content])
        self.setItem(row, 4, QTableWidgetItem(binary_content))

    def copySelectionToClipboard(self):
        selected_ranges = self.selectedRanges()
        if not selected_ranges:
            return

        copied_text = []
        
        for selection in selected_ranges:
            rows = []
            for row in range(selection.topRow(), selection.bottomRow() + 1):
                cols = []
                for col in range(selection.leftColumn(), selection.rightColumn() + 1):
                    item = self.item(row, col)
                    cols.append(item.text() if item else "")  # Get text or empty string if None
                rows.append("\t".join(cols))  # Separate columns by tab (Excel format)
            copied_text.append("\n".join(rows))  # Separate rows by new line

        clipboard = QApplication.clipboard()
        clipboard.setText("\n".join(copied_text))  # Copy formatted text to clipboard

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copySelectionToClipboard()
        else:
            super().keyPressEvent(event)

    def highlightChange(self, row, column, color):
        item = self.item(row, column)
        if not item:
            return

        # Get the original background color (handles dark/light mode properly)
        default_color = self.palette().color(QPalette.ColorRole.Base)
        
        # If item already has a custom background, use it
        original_color = item.background().color()
        if not original_color.isValid() or original_color == QColor(0, 0, 0):  
            original_color = default_color  

        item.setBackground(color)

        # Restore original color after 500ms
        QTimer.singleShot(500, lambda: self.resetCellColor(row, column, original_color))

    def resetCellColor(self, row, column, color):
        self.blockSignals(True)
        item = self.item(row, column)
        if item:
            item.setBackground(color)
        self.blockSignals(False)
