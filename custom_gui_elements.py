"""
This file containst gustom GUI structures which are then later used in main gui
file
"""

from datatypes import Data
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QTextCursor, QPainter, QColor, QTextFormat
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QCheckBox,
    QMessageBox,
    QPlainTextEdit
)

alg_cent =      Qt.AlignmentFlag.AlignCenter
alg_right =     Qt.AlignmentFlag.AlignRight
alg_top =       Qt.AlignmentFlag.AlignTop
alg_jst =       Qt.AlignmentFlag.AlignJustify
ok_button =     QMessageBox.StandardButton.Ok
cancel_button = QMessageBox.StandardButton.Cancel

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
        register_label = QLabel(register_name)
        register_label.setStyleSheet(f"color: {text_color};")
        font = QFont() ; font.setBold(True) ; font.setPointSize(15)
        register_label.setFont(font)
        row_layout.addWidget(register_label)
        register_label.setToolTip(f'<span style="color: white;">\
            {"General purpose register" if not custom_name else custom_name}\
            </span>')
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
        self.register_high_bits.setReadOnly(True)
        self.register_high_bits.setAlignment(alg_cent)
        text_field_layout.addWidget(self.register_high_bits)

        self.register_low_bits = QLineEdit()
        self.register_low_bits.setStyleSheet("QLineEdit { letter-spacing: 1px; }")
        self.register_low_bits.setInputMask("BBBBBBBB")  # 8-bitowa wartość binarna
        self.register_low_bits.setFixedWidth(90)  # Adjust for 8 characters
        self.register_low_bits.setReadOnly(True)
        self.register_low_bits.setAlignment(alg_cent)
        text_field_layout.addWidget(self.register_low_bits)

        main_field_layout.addLayout(text_field_layout)

        # Add main_field_layout to the row layout
        row_layout.addLayout(main_field_layout)

        # Equals label
        equals_label = QLabel("=")
        row_layout.addWidget(equals_label)

        # Smaller text field (8 characters wide)
        self.register_decimal_value = QLineEdit()
        self.register_decimal_value.setFixedWidth(60)  # Adjust width as needed
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


class FunctionalRegisters(QWidget):
    def __init__(self, HR, register_name, text_color = 'white', custom_name = ''):
        super().__init__()

        self.register_name = register_name
        self.HR = HR

        row_layout = QHBoxLayout()

        register_label = QLabel(register_name)
        register_label.setFixedWidth(30)
        register_label.setStyleSheet(f"color: {text_color};")
        font = QFont() ; font.setBold(True) ; font.setPointSize(15)
        register_label.setFont(font)
        row_layout.addWidget(register_label)
        register_label.setToolTip(
            f'{"Special register" if not custom_name else custom_name}')

        self.register_content = QLineEdit()
        self.register_content.setStyleSheet("QLineEdit { letter-spacing: 1px; }")
        self.register_content.setFixedWidth(180)
        self.register_content.setReadOnly(True)
        self.register_content.setAlignment(alg_cent)
        row_layout.addWidget(self.register_content)

        # Equals label
        equals_label = QLabel("=")
        row_layout.addWidget(equals_label)

        # Smaller text field (8 characters wide)
        self.register_decimal_value = QLineEdit()
        self.register_decimal_value.setFixedWidth(60)  # Adjust width as needed
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


class FlagRegister(QWidget):
    """
    This class is responsible for display of flag register = it containts a text
    field with source value, and below it, there are checkbox'es working like 
    indicators for all flags which are important for the user
    """

    def __init__(self, FR):
        super().__init__()

        self.FR = FR

        wrapper = QHBoxLayout()
        body = QFormLayout()
        firts_row = QHBoxLayout()
        register_label = QLabel("FLAGS")
        register_label.setStyleSheet("color: #30BB73;")
        font = QFont() ; font.setBold(True) ; font.setPointSize(15)
        register_label.setFont(font)
        firts_row.addWidget(register_label)
        firts_row.insertSpacing(1,20)

        self.register_content = QLineEdit()
        self.register_content.setStyleSheet("QLineEdit { letter-spacing: 1px; }")
        self.register_content.setFixedWidth(200)
        self.register_content.setReadOnly(True)
        self.register_content.setAlignment(alg_cent)
        firts_row.addWidget(self.register_content)

        self.flag_indicators_row_1 = QHBoxLayout()
        self.flag_indicators_row_2 = QHBoxLayout()
        self.flag_indicators_row_3 = QHBoxLayout()

        #   Define all flags, in order they should be displayed
        self.overflow_flag          = CustomQCheckBox('Overflow')
        self.direction_flag         = CustomQCheckBox('Direction')
        self.interrupt_flag         = CustomQCheckBox('Interrrupt')
        self.trap_flag              = CustomQCheckBox('Trap')
        self.sign_flag              = CustomQCheckBox('Sign')
        self.zero_flag              = CustomQCheckBox('Zero')
        self.auxiliary_carry_flag   = CustomQCheckBox('Auxiliary carry')
        self.parity_flag            = CustomQCheckBox('Parity')
        self.carry_flag             = CustomQCheckBox('Carry')

        #   Automatically assign all flags it's definitions defined in FlagRegister file,
        # so that it will be displeyd when user hovers cousor over the checkbox
        for attr_name in dir(self):
            if attr_name.endswith('_flag'):
                attr_value = getattr(self, attr_name)
                definition = getattr(FR, f"def_{attr_name}")
                attr_value.setToolTip(f'{definition()}')
                attr_value.setModifiable(False)
                # self.flag_indicators_row_1.addWidget(attr_value)

        self.flag_indicators_row_1.addWidget(self.overflow_flag)
        self.flag_indicators_row_1.insertSpacing(1,30)
        self.flag_indicators_row_1.addWidget(self.direction_flag)
        self.flag_indicators_row_1.insertSpacing(3,30)
        self.flag_indicators_row_1.addWidget(self.interrupt_flag)

        self.flag_indicators_row_2.addWidget(self.trap_flag)
        self.flag_indicators_row_2.insertSpacing(1,30)
        self.flag_indicators_row_2.addWidget(self.sign_flag)
        self.flag_indicators_row_2.insertSpacing(3,30)
        self.flag_indicators_row_2.addWidget(self.zero_flag)

        self.flag_indicators_row_3.addWidget(self.auxiliary_carry_flag)
        self.flag_indicators_row_3.addWidget(self.parity_flag)
        self.flag_indicators_row_3.insertSpacing(2,30)
        self.flag_indicators_row_3.addWidget(self.carry_flag)

        self.flag_indicators_row_1.setStretch(0, 1)
        self.flag_indicators_row_2.setStretch(1, 2)
        self.flag_indicators_row_3.setStretch(2, 3)
        body.addRow(firts_row)
        body.addRow(self.flag_indicators_row_1)
        body.addRow(self.flag_indicators_row_2)
        body.addRow(self.flag_indicators_row_3)
        # firts_row.setStretch(0, 1)  # Stretch the layout for register label
        # firts_row.setStretch(1, 2)  # Stretch the layout for register content field

        wrapper.addLayout(body)   
        # wrapper.setStretch(1,1)     

        self.setLayout(wrapper)
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


class Terminal(QWidget):
    def __init__(self):
        super().__init__()

        main_frame = QFormLayout()
        
        label = QLabel('Terminal')
        font = QFont() ; font.setBold(True) ; font.setPointSize(15)
        label.setFont(font)
        # main_frame.addWidget(label)

        self.terminal = QTextEdit()
        font = QFont() ; font.setBold(True) ; font.setPointSize(12)
        self.terminal.setFont(font)
        self.terminal.setMinimumHeight(160)
        # main_frame.addWidget(terminal)

        main_frame.addRow(label)
        main_frame.addRow(self.terminal)

        self.setLayout(main_frame)

    def write_char(self, char : int):
        text = self.terminal.toPlainText()
        print(chr(char), end="", flush=True)
        self.terminal.setPlainText(text + chr(char))

class CustomQCheckBox(QCheckBox):
    """
    This code is based on code provided by user Luis E. on StackOverflow forum
    Date of access: 11.11.2024
    Link to source: https://stackoverflow.com/questions/11472284/how-to-set-a-read-only-checkbox-in-pyside-pyqt
    """

    def __init__(self, *args):
        QCheckBox.__init__(self, *args)        
        self.is_modifiable = True
        self.clicked.connect( self.modify_on_click )

    def modify_on_click(self): 
        if self.isChecked():
            self.setChecked(self.is_modifiable)
        else:
            self.setChecked(not self.is_modifiable)            

    def setModifiable(self, flag):
        self.is_modifiable = flag            

    def isModifiable(self):
        return self.is_modifiable


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.myeditor = editor

    def sizeHint(self):
        return self.myeditor.line_number_area_width(), 0

    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)


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

    def lineNumberAreaPaintEvent(self, event):
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


class StackEditor(QPlainTextEdit):

    def __init__(self, data : Data):
        super().__init__()
        self.data = data
        self.setFixedWidth(210)
        self.bits = []
        
    def update(self):

        def format_line(line):
            return f"{str(hex(line[0])[2:]).zfill(4)})\t{bin(line[1])[2:].zfill(8)} = {line[1]}"

        fresh_stack = self.data.data[:]
        fresh_stack.reverse()
        if self.bits != fresh_stack:
            numbered_line_pairs = zip(range(2**16-1,-1,-1), fresh_stack)
            self.setPlainText("\n".join(map(format_line, numbered_line_pairs)))


class VariableEditor(QPlainTextEdit):

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.setMinimumWidth(300)
        self.bits = []
        
    def update(self):

        variables = self.engine.variables
        data = self.engine.data

        end_text = f"#\tsize\t{'name':10}\taddres\tcontent\n\n"
        
        if variables == None:
            self.setPlainText(end_text)
            return

        def format_line(pair):
            line, variable = pair
            address, size, format = variables[variable].values()
            content = data.get_data(address, size)
            divided_content = []
            for i in range(0, len(content)-1, 8):
                raw_content_part = [str(b) for b in content[i : i+8]]
                divided_content.append("".join(raw_content_part))
            formatted_content = " ".join(divided_content)
            return f"{line}\t{size}\t{variable:10}\t{address}\t{formatted_content}"

        end_text += "\n".join(map(format_line, enumerate(variables)))

        self.setPlainText(end_text)
