"""
This file containst gustom GUI structures which are then later used in main gui
file
"""

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QTextCursor, QPainter, QColor, QTextFormat, QValidator
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
from flag_register import FlagRegister as FR

alg_cent =      Qt.AlignmentFlag.AlignCenter
alg_right =     Qt.AlignmentFlag.AlignRight
alg_top =       Qt.AlignmentFlag.AlignTop
alg_jst =       Qt.AlignmentFlag.AlignJustify
ok_button =     QMessageBox.StandardButton.Ok
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
        # self.register_upper_bits = QLineEdit()
        # self.register_upper_bits.setFixedWidth(140)  # Adjust for 16 characters
        # self.register_upper_bits.setAlignment(alg_right)
        # self.register_upper_bits.setReadOnly(True)
        # text_field_layout.addWidget(self.register_upper_bits)

        self.register_high_bits = QLineEdit()
        self.register_high_bits.setInputMask("BBBBBBBB")  # 8-bitowa wartość binarna
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

    def get_name(self):
        return self.name
    
    def set_interactive(self, value : bool = False):
        # self.register_upper_bits.setReadOnly(not value) # uncomment this line for 32
        self.register_high_bits.setReadOnly(not value)
        self.register_low_bits.setReadOnly(not value)
        self.register_decimal_value.setReadOnly(not value)

class FunctionalRegisters(QWidget):
    def __init__(self, register_name, text_color = 'white', custom_name = ''):
        super().__init__()

        self.register_name = register_name

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
        self.register_content.setFixedWidth(140)
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

    def get_name(self):
        return self.register_name

    def set_interactive(self, value : bool = False):
        self.register_content.setReadOnly(not value)

class FlagRegister(QWidget):

    def __init__(self):
        super().__init__()

        wrapper = QHBoxLayout()
        body = QFormLayout()
        firts_row = QHBoxLayout()
        register_label = QLabel("FLAGS")
        register_label.setStyleSheet("color: #30BB73;")
        font = QFont() ; font.setBold(True) ; font.setPointSize(15)
        register_label.setFont(font)
        firts_row.addWidget(register_label)

        self.register_content = QLineEdit()
        self.register_content.setFixedWidth(140)
        self.register_content.setReadOnly(True)
        self.register_content.setAlignment(alg_cent)
        firts_row.addWidget(self.register_content)
        firts_row.setStretch(0, 1)

        self.flag_indicators_row_1 = QHBoxLayout()
        self.flag_indicators_row_1.addStretch()
        self.flag_indicators_row_2 = QHBoxLayout()
        self.flag_indicators_row_2.addStretch()
        self.overflow_flag          = CustomQCheckBox('OF')
        self.direction_flag         = CustomQCheckBox('DF')
        self.interrupt_flag         = CustomQCheckBox('IF')
        self.trap_flag              = CustomQCheckBox('TF')
        self.sign_flag              = CustomQCheckBox('SF')
        self.zero_flag              = CustomQCheckBox('ZF')
        self.auxiliary_carry_flag   = CustomQCheckBox('AF')
        self.parity_flag            = CustomQCheckBox('PF')
        self.carry_flag             = CustomQCheckBox('CF')

        tmp = 0

        for attr_name in dir(self):
            if attr_name.endswith('_flag'):
                attr_value = getattr(self, attr_name)
                definition = getattr(FR(), f"def_{attr_name}")
                attr_value.setToolTip(f'{definition()}')
                attr_value.setModifiable(False)
                if tmp < 5:
                    self.flag_indicators_row_1.addWidget(attr_value)
                else:
                    self.flag_indicators_row_2.addWidget(attr_value)
                tmp += 1

        self.flag_indicators_row_1.setStretch(0, 1)
        self.flag_indicators_row_2.setStretch(1, 1)
        body.addRow(firts_row)
        body.addRow(self.flag_indicators_row_1)
        body.addRow(self.flag_indicators_row_2)
        firts_row.setStretch(0, 1)  # Stretch the layout for register label
        firts_row.setStretch(1, 2)  # Stretch the layout for register content field

        wrapper.addLayout(body)   
        wrapper.setStretch(1,1)     

        self.setLayout(wrapper)
        self._setRegisterValue(4)

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

    
    def get_name(self):
        return "FLAGS"
    
    def set_interactive(self, value : bool = False):
        for attr_name in dir(self):
            if attr_name.endswith('_flag'):
                attr_value = getattr(self, attr_name)
                attr_value.setModifiable(value)
        self.register_content.setReadOnly(not value)

# class FlagRegister(QWidget):
#     def __init__(self):
#         super().__init__()

#         wrapper = QVBoxLayout()
#         body = QVBoxLayout()  # Zmieniono na QVBoxLayout, aby łatwiej zarządzać rzędami.
        
#         # Pierwszy rząd: labelka FLAGS i pole tekstowe
#         firts_row = QHBoxLayout()
#         register_label = QLabel("FLAGS")
#         register_label.setStyleSheet("color: #30BB73;")
#         font = QFont()
#         font.setBold(True)
#         font.setPointSize(15)
#         register_label.setFont(font)
#         firts_row.addWidget(register_label)
#         firts_row.addStretch()  # Dodaje przestrzeń między elementami
#         self.register_content = QLineEdit()
#         self.register_content.setFixedWidth(240)
#         self.register_content.setReadOnly(True)
#         self.register_content.setAlignment(alg_right)  # Wyrównanie do prawej
#         firts_row.addWidget(self.register_content)
#         firts_row.setStretch(0, 1)  # FLAGS rozciąga się na lewo
#         firts_row.setStretch(2, 2)  # register_content rozciąga się na prawo
#         body.addLayout(firts_row)

#         # Rzędy dla flag
#         self.flag_indicators_row_1 = QHBoxLayout()
#         self.flag_indicators_row_2 = QHBoxLayout()

#         # Dodanie flag do rzędów
#         flags = [
#             ('OF', 'overflow_flag'),
#             ('DF', 'direction_flag'),
#             ('IF', 'interrupt_flag'),
#             ('TF', 'trap_flag'),
#             ('SF', 'sign_flag'),
#             ('ZF', 'zero_flag'),
#             ('AF', 'auxiliary_carry_flag'),
#             ('PF', 'parity_flag'),
#             ('CF', 'carry_flag')
#         ]

#         for idx, (label, attr_name) in enumerate(flags):
#             checkbox = CustomQCheckBox(label)
#             setattr(self, attr_name, checkbox)
#             if idx < 5:
#                 self.flag_indicators_row_1.addWidget(checkbox)
#             else:
#                 self.flag_indicators_row_2.addWidget(checkbox)

#         # Rozciąganie flag w rzędach
#         for row in [self.flag_indicators_row_1, self.flag_indicators_row_2]:
#             row.addStretch(0)  # Wypełniacz po lewej
#             row.addStretch()   # Wypełniacz po prawej

#         self.flag_indicators_row_1.setSpacing(10)
#         self.flag_indicators_row_1.addStretch(1)  # Wypełniacz na końcu
#         self.flag_indicators_row_2.setSpacing(10)
#         self.flag_indicators_row_2.addStretch(1)

#         body.addLayout(self.flag_indicators_row_1)
#         body.addLayout(self.flag_indicators_row_2)

#         # Ustawienia głównego układu
#         wrapper.addLayout(body)
#         self.setLayout(wrapper)

#         # Ustawienie początkowej wartości rejestru
#         self._setRegisterValue(4)

#     def _setRegisterValue(self, value : int | list | str):
#         """This method sets value as bits in register"""
        
#         if type(value) == list:                  # Put this value for 32 bit mode
#             if len(value) < 16:                             # 32
#                 while len(value) < 16:                      # 32
#                     value.insert(0,0)
#             if len(value) > 16:                             # 32
#                 value = value[-16:]                         # -32
#             value = "".join((str(x) for x in value))

#         elif type(value) == int:
#             if value >= 2**16 or value <= -(2**8):         # 2**32 | 2**16
#                 value %= 2**16+1                           # 2**32 + 1
#             value = bin(value)[2:]
        
#         assert type(value) == str
#         value = value.zfill(16)                            # 32

#         self.register_content.setText(value)

#         self.overflow_flag.         setChecked(value[-12] == "1")
#         self.direction_flag.        setChecked(value[-11] == "1")
#         self.interrupt_flag.        setChecked(value[-10] == "1")
#         self.trap_flag.             setChecked(value[-9] == "1")
#         self.sign_flag.             setChecked(value[-8] == "1")
#         self.zero_flag.             setChecked(value[-7] == "1")
#         self.auxiliary_carry_flag.  setChecked(value[-5] == "1")
#         self.parity_flag.           setChecked(value[-3] == "1")
#         self.carry_flag.            setChecked(value[-1] == "1")


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
                 background_color=Qt.GlobalColor.blue, 
                 text_color=Qt.GlobalColor.white):
        """
        Podświetla wybrane linie i przewija widok, aby podświetlona linia była na środku.

        Args:
            line_numbers (list[int]): Lista numerów linii do podświetlenia (1-based).
            background_color (QColor): Kolor tła dla podświetlenia.
            text_color (QColor): Kolor tekstu w podświetlonych liniach.
        """
        # Tworzymy listę podświetlonych obiektów
        extraSelections = []

        # Przechodzimy po liniach do podświetlenia
        for line_number in line_numbers:
            if line_number <= 0:
                continue

            # Ustawiamy kursor na początku odpowiedniej linii
            cursor = QTextCursor(self.document().findBlockByLineNumber(line_number - 1))
            if not cursor.isNull():
                selection = QTextEdit.ExtraSelection()

                # Konfiguracja tła
                selection.format.setBackground(QColor(background_color))
                selection.format.setForeground(QColor(text_color))
                selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
                selection.cursor = cursor
                selection.cursor.clearSelection()

                # Dodajemy do listy podświetleń
                extraSelections.append(selection)

                # Przechowujemy informacje o podświetlonych liniach
                self.highlighted_lines = line_numbers

                # Aktualizacja podświetleń w edytorze
                self.setExtraSelections(extraSelections)

                # Automatyczne przewijanie
                if line_numbers:
                    # Wybieramy pierwszą linię z listy jako priorytet przewijania
                    target_line = line_numbers[0]
                    block = self.document().findBlockByLineNumber(target_line - 1)
                    if block.isValid():
                        block_top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
                        block_height = self.blockBoundingRect(block).height()
                        
                        # Obliczamy środek widoku
                        viewport_height = self.viewport().height()
                        target_center = block_top - (viewport_height // 2) + (block_height // 2)

                        # Przewijamy, ustawiając linię na środku widoku
                        vertical_scroll_bar = self.verticalScrollBar()
                        vertical_scroll_bar.setValue(int(target_center))

        # Przechowujemy informacje o podświetlonych liniach
        self.highlighted_lines = line_numbers

        # Aktualizacja podświetleń w edytorze
        self.setExtraSelections(extraSelections)

    def setText(self, text):
        self.setPlainText(text)

    def setEditable(self, editable):
        self.setReadOnly(not editable)
