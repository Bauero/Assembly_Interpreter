"""
This file containst gustom GUI structures which are then later used in main gui
file
"""

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

alg_cent = Qt.AlignmentFlag.AlignCenter
alg_right = Qt.AlignmentFlag.AlignRight
alg_top = Qt.AlignmentFlag.AlignTop
alg_jst = Qt.AlignmentFlag.AlignJustify
ok_button = QMessageBox.StandardButton.Ok
cancel_button = QMessageBox.StandardButton.Cancel

################################################################################
#   Clasess with custom gui structures
################################################################################

class MultipurposeRegister(QWidget):
    """This class creates a widget for displaying multipurpose register, splited into
    high and low bits as well as a dedicated field for displaying decimal value of register
    """

    def __init__(self, register_name, text_color = 'white', custom_name = ''):
        super().__init__()

        self.name = register_name
        
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
        
        # Container for the H and L labels and main text fields
        main_field_layout = QVBoxLayout()

        # Main text fields in a horizontal layout with no spacing
        text_field_layout = QHBoxLayout()
        text_field_layout.setSpacing(0)  # No gaps between fields

        # Three separate text fields with widths for 16, 8, and 8 characters
        self.register_upper_bits = QLineEdit()
        self.register_upper_bits.setFixedWidth(140)  # Adjust for 16 characters
        self.register_upper_bits.setAlignment(alg_right)
        self.register_upper_bits.setReadOnly(True)
        text_field_layout.addWidget(self.register_upper_bits)

        self.register_high_bits = QLineEdit()
        self.register_high_bits.setFixedWidth(70)  # Adjust for 8 characters
        self.register_high_bits.setReadOnly(True)
        self.register_high_bits.setAlignment(alg_cent)
        text_field_layout.addWidget(self.register_high_bits)

        self.register_low_bits = QLineEdit()
        self.register_low_bits.setFixedWidth(70)  # Adjust for 8 characters
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
        self.register_decimal_value.setFixedWidth(100)  # Adjust width as needed
        self.register_decimal_value.setReadOnly(True)
        self.register_decimal_value.setAlignment(alg_cent)
        row_layout.addWidget(self.register_decimal_value)
        
        # Set the layout for this widget
        self.setLayout(row_layout)
        self._setRegisterValue(0)

    def _setRegisterValue(self, value : int | list | str):
        """This method sets value as bits in register"""
        
        if type(value) == list:
            if len(value) < 32:
                while len(value) < 32:
                    value.insert(0,0)
            if len(value) > 32:
                value = value[-32:-1]
            value = "".join((str(x) for x in value))

        elif type(value) == int:
            if value >= 2**32 or value <= -(2**16):
                value %= 2**32+1
            value = bin(value)[2:]
        
        assert type(value) == str
        value = value.zfill(32)

        self.register_upper_bits.setText(value[:16])
        self.register_high_bits.setText(value[16:24])
        self.register_low_bits.setText(value[24:])
        self.register_decimal_value.setText(f"{int(value, base=2)}")

class FunctionalRegisters(QWidget):
    def __init__(self, register_name, text_color = 'white', custom_name = ''):
        super().__init__()

        row_layout = QHBoxLayout()

        register_label = QLabel(register_name)
        register_label.setFixedWidth(30)
        register_label.setStyleSheet(f"color: {text_color};")
        font = QFont() ; font.setBold(True) ; font.setPointSize(15)
        register_label.setFont(font)
        row_layout.addWidget(register_label)
        register_label.setToolTip(
            f'<span style="color: white;">\
            {"Special register" if not custom_name else custom_name}\
            </span>')

        self.register_content = QLineEdit()
        self.register_content.setFixedWidth(280)
        self.register_content.setReadOnly(True)
        self.register_content.setAlignment(alg_cent)
        row_layout.addWidget(self.register_content)

        # Equals label
        equals_label = QLabel("=")
        row_layout.addWidget(equals_label)

        # Smaller text field (8 characters wide)
        self.register_decimal_value = QLineEdit()
        self.register_decimal_value.setFixedWidth(100)  # Adjust width as needed
        self.register_decimal_value.setReadOnly(True)
        self.register_decimal_value.setAlignment(alg_cent)
        row_layout.addWidget(self.register_decimal_value)

        self.setLayout(row_layout)
        self._setRegisterValue(0)

    def _setRegisterValue(self, value : int | list | str):
        """This method sets value as bits in register"""
        
        if type(value) == list:
            if len(value) < 32:
                while len(value) < 32:
                    value.insert(0,0)
            if len(value) > 32:
                value = value[-32:-1]
            value = "".join((str(x) for x in value))

        elif type(value) == int:
            if value >= 2**32 or value < -(2**31):
                value %= 2**32+1
            value = bin(value)[2:]
        
        assert type(value) == str
        value = value.zfill(32)

        self.register_content.setText(value)
        self.register_decimal_value.setText(f"{int(value, base=2)}")

class FlagRegister(QWidget):

    def __init__(self):
        super().__init__()

        body = QFormLayout()
    
        firts_row = QHBoxLayout()

        register_label = QLabel("EFLAGS")
        # register_label.setFixedWidth(30)
        register_label.setStyleSheet("color: #30BB73;")
        font = QFont() ; font.setBold(True) ; font.setPointSize(15)
        register_label.setFont(font)
        firts_row.addWidget(register_label)

        self.register_content = QLineEdit()
        self.register_content.setFixedWidth(280)
        self.register_content.setReadOnly(True)
        self.register_content.setAlignment(alg_cent)
        firts_row.addWidget(self.register_content)

        self.flag_indicators = QHBoxLayout()
        self.flag_indicators.addStretch()
        self.overflow_flag          = CustomQCheckBox('OF')
        self.direction_flag         = CustomQCheckBox('DF')
        self.interrupt_flag         = CustomQCheckBox('IF')
        self.trap_flag              = CustomQCheckBox('TF')
        self.sign_flag              = CustomQCheckBox('SF')
        self.zero_flag              = CustomQCheckBox('ZF')
        self.auxiliary_carry_flag   = CustomQCheckBox('AF')
        self.parity_flag            = CustomQCheckBox('PF')
        self.carry_flag             = CustomQCheckBox('CF')

        self.overflow_flag.setModifiable(False)
        self.direction_flag.setModifiable(False)
        self.interrupt_flag.setModifiable(False)
        self.trap_flag.setModifiable(False)
        self.sign_flag.setModifiable(False)
        self.zero_flag.setModifiable(False)
        self.auxiliary_carry_flag.setModifiable(False)
        self.parity_flag.setModifiable(False)
        self.carry_flag.setModifiable(False)

        self.flag_indicators.addWidget(self.overflow_flag)
        self.flag_indicators.addWidget(self.direction_flag)
        self.flag_indicators.addWidget(self.interrupt_flag)
        self.flag_indicators.addWidget(self.trap_flag)
        self.flag_indicators.addWidget(self.sign_flag)
        self.flag_indicators.addWidget(self.zero_flag)
        self.flag_indicators.addWidget(self.auxiliary_carry_flag)
        self.flag_indicators.addWidget(self.parity_flag)
        self.flag_indicators.addWidget(self.carry_flag)

        
        body.addRow(firts_row)
        body.addRow(self.flag_indicators)
        firts_row.setStretch(0, 1)  # Stretch the layout for register label
        firts_row.setStretch(1, 2)  # Stretch the layout for register content field
        self.flag_indicators.setStretch(1, 1)
        
        self.setLayout(body)
        self._setRegisterValue(4)

    def _setRegisterValue(self, value : int | list | str):
        """This method sets value as bits in register"""
        
        if type(value) == list:
            if len(value) < 32:
                while len(value) < 32:
                    value.insert(0,0)
            if len(value) > 32:
                value = value[-32:-1]
            value = "".join((str(x) for x in value))

        elif type(value) == int:
            if value >= 2**32 or value < -(2**31):
                value %= 2**32+1
            value = bin(value)[2:]
        
        assert type(value) == str
        value = value.zfill(32)

        self.register_content.setText(value)

        print(value[31])

        self.overflow_flag.         setChecked(value[20] == "1")
        self.direction_flag.        setChecked(value[21] == "1")
        self.interrupt_flag.        setChecked(value[22] == "1")
        self.trap_flag.             setChecked(value[23] == "1")
        self.sign_flag.             setChecked(value[24] == "1")
        self.zero_flag.             setChecked(value[25] == "1")
        self.auxiliary_carry_flag.  setChecked(value[27] == "1")
        self.parity_flag.           setChecked(value[29] == "1")
        self.carry_flag.            setChecked(value[31] == "1")

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
        return self.myeditor.lineNumberAreaWidth(), 0

    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        # self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.textCursor().movePosition(QTextCursor.MoveOperation.Start)  # Przesuń kursor na początek
        # self.highlightCurrentLine()

        self.highlighted_lines = []

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count //= 10
            digits += 1
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy != 0:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        # painter.fillRect(event.rect(), Qt.GlobalColor.gray)

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

    # def highlightCurrentLine(self):
    #     # Tworzymy obiekt do przechowywania podświetlonych elementów
    #     extraSelections = []

    #     if not self.isReadOnly():
    #         # Tworzymy obiekt selekcji
    #         selection = QTextEdit.ExtraSelection()

    #         # Ustawienia koloru tła
    #         lineColor = QColor(Qt.GlobalColor.blue)  # Jasno żółty
    #         selection.format.setBackground(lineColor)

    #         # Ustawienia koloru tekstu
    #         textColor = QColor(Qt.GlobalColor.white)  # Czerwony kolor tekstu
    #         selection.format.setForeground(textColor)

    #         # Ustawienie właściwości, aby podświetlać pełną szerokość linii
    #         selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)

    #         # Ustawienie bieżącego bloku (linii)
    #         selection.cursor = self.textCursor()
    #         selection.cursor.clearSelection()

    #         # Dodanie selekcji do listy
    #         extraSelections.append(selection)

    #     # Przypisujemy listę podświetlonych elementów do edytora
    #     self.setExtraSelections(extraSelections)

    def setHighlight(self, line_numbers, 
                     background_color =  Qt.GlobalColor.blue, 
                     text_color =        Qt.GlobalColor.white):
        """
        Podświetla wybrane linie.
        
        Args:
            line_numbers (list[int]): Lista numerów linii do podświetlenia (1-based).
            background_color (QColor): Kolor tła dla podświetlenia.
            text_color (QColor): Kolor tekstu w podświetlonych liniach.
        """
        # Tworzymy listę podświetlonych obiektów
        extraSelections = []

        # Przechodzimy po liniach do podświetlenia
        for line_number in line_numbers:
            # Upewniamy się, że numer linii jest poprawny
            if line_number <= 0:
                continue

            # Ustawiamy kursor na początku odpowiedniej linii
            cursor = QTextCursor(self.document().findBlockByLineNumber(line_number - 1))
            if not cursor.isNull():
                selection = QTextEdit.ExtraSelection()

                # Konfiguracja tła
                selection.format.setBackground(QColor(background_color))

                # Konfiguracja tekstu
                selection.format.setForeground(QColor(text_color))

                # Pełne podświetlenie linii
                selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)

                # Ustawienie kursora dla tej linii
                selection.cursor = cursor
                selection.cursor.clearSelection()  # Podświetlamy całą linię bez selekcji

                # Dodajemy do listy podświetleń
                extraSelections.append(selection)

        # Przechowujemy informacje o podświetlonych liniach
        self.highlighted_lines = line_numbers

        # Aktualizacja podświetleń w edytorze
        self.setExtraSelections(extraSelections)

    def setText(self, text):
        self.setPlainText(text)

    def setEditable(self, editable):
        self.setReadOnly(not editable)