"""
This file containst gustom GUI structures which are then later used in main gui
file
"""

from .engine import Engine
from .hardware_memory import DataSegment
from .flag_register import FlagRegister
from .helper_functions import return_name_from_size, color_txt
from .custom_message_boxes import show_custom_popup
from PyQt6.QtCore import Qt, QRect, QTimer, pyqtSignal
from PyQt6.QtGui import (
    QFont, QTextCursor, QPainter, QColor, QTextFormat, QKeySequence, QPalette,
    QKeyEvent)
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QHBoxLayout, QLineEdit, QTextEdit,
    QMessageBox, QPlainTextEdit, QTableWidget, QHeaderView, QTableWidgetItem, 
    QAbstractItemView,QApplication)
import json

with open('program_code/color_palette.json') as f:  colors = json.load(f)
with open('program_code/names.json') as f:
    all_conumicates = json.load(f)
    supported_languages = all_conumicates["supported_languages"]
    lang_names_each_other = all_conumicates["lang_names_each_other"]
    names = all_conumicates["language_presets"]

alg_cent =      Qt.AlignmentFlag.AlignCenter
alg_right =     Qt.AlignmentFlag.AlignRight
alg_top =       Qt.AlignmentFlag.AlignTop
alg_jst =       Qt.AlignmentFlag.AlignJustify

ok_button =     QMessageBox.StandardButton.Ok
cancel_button = QMessageBox.StandardButton.Cancel

bold_16 = QFont() ; bold_16.setBold(True) ; bold_16.setPointSize(16)
bold_italic_15 = QFont() ; bold_italic_15.setBold(True)
bold_italic_15.setItalic(True) ; bold_italic_15.setPointSize(15)
font_15 = QFont() ; font_15.setPointSize(15)

register_text_style = "QLineEdit { letter-spacing: 1px; }"
table_grid = "QTableWidget {gridline-color: #606060; letter-spacing: 1px; font-size: 13px}"
input_mask_8 = "BBBBBBBB"
width_int = 60
width_8_bit = 90
width_16_bit = 2 * width_8_bit
register_height = 20
reg_label_width = 30
no_spacing = 0

class MultipurposeRegister(QWidget):
    """This class creates a widget for displaying multipurpose register, splited into
    high and low bits as well as a dedicated field for displaying decimal value of register
    """

    def __init__(self, HR, register_name : str, language : str, theme : str):
        super().__init__()

        self.HR = HR
        self.register_name = register_name
        self.language = language
        self.theme = theme
        row_layout = QHBoxLayout()
        split_reg_widget = QWidget()
        split_reg_layout = QHBoxLayout()
        
        self.register_label = QLabel(register_name)
        self.register_label.setStyleSheet(f'color: {colors[self.theme]["multipurpose_registers"]};')
        self.register_label.setFont(bold_16)
        self.register_label.setToolTip(color_txt(
                                        names[self.language][f"{self.register_name}_hint"],
                                        colors[theme]["hints"]))
        self.register_label.setFixedWidth(reg_label_width)
        self.register_label.setFixedHeight(register_height)

        self.register_high_bits = QLineEdit()
        self.register_high_bits.setStyleSheet(register_text_style)
        self.register_high_bits.setInputMask(input_mask_8)
        self.register_high_bits.setFixedWidth(width_8_bit)
        self.register_high_bits.setFixedHeight(register_height)
        self.register_high_bits.setReadOnly(True)
        self.register_high_bits.setAlignment(alg_cent)

        self.register_low_bits = QLineEdit()
        self.register_low_bits.setStyleSheet(register_text_style)
        self.register_low_bits.setInputMask(input_mask_8)
        self.register_low_bits.setFixedWidth(width_8_bit)
        self.register_low_bits.setFixedHeight(register_height)
        self.register_low_bits.setReadOnly(True)
        self.register_low_bits.setAlignment(alg_cent)

        equals_label = QLabel("=")
        equals_label.setFixedHeight(register_height)

        self.register_decimal_value = QLineEdit()
        self.register_decimal_value.setFixedWidth(width_int)
        self.register_decimal_value.setFixedHeight(register_height)
        self.register_decimal_value.setReadOnly(True)
        self.register_decimal_value.setAlignment(alg_cent)
        
        split_reg_layout.addWidget(self.register_high_bits)
        split_reg_layout.addWidget(self.register_low_bits)
        split_reg_widget.setLayout(split_reg_layout)
        
        row_layout.addWidget(self.register_label)
        row_layout.addWidget(split_reg_widget)
        row_layout.addWidget(equals_label)
        row_layout.addWidget(self.register_decimal_value)
        
        split_reg_layout.setContentsMargins(0,0,0,0)
        split_reg_layout.setSpacing(no_spacing)
        row_layout.insertSpacing(4,1)
        
        self.setLayout(row_layout)
        self.update()

    def _setRegisterValue(self, value : str):
        value = value.zfill(16)[-16:]
        self.register_high_bits.setText(value[-16:-8])
        self.register_low_bits.setText(value[-8:])
        self.register_decimal_value.setText(f"{int(value, base=2)}")

    def update(self):
        self._setRegisterValue(self.HR.readFromRegister(self.register_name))

    def get_name(self) -> str:
        return self.register_name
    
    def set_interactive(self, value : bool = False):
        self.register_high_bits.setReadOnly(not value)
        self.register_low_bits.setReadOnly(not value)
        self.register_decimal_value.setReadOnly(not value)

    def set_hint(self, language : str):
        self.language = language
        name = f"{self.register_name}_hint"
        self.register_label.setToolTip(color_txt(
            names[self.language][name], colors[self.theme]["hints"]))

    def change_theme(self, theme : str):
        current_hint = self.register_label.toolTip()
        self.theme = theme
        self.register_label.setToolTip(color_txt(current_hint, colors[self.theme]["hints"]))


class FunctionalRegisters(QWidget):
    """
    This class displays functional registers, which don't have upper and lower subregisters
    """
    
    def __init__(self, HR, register_name : str, language : str, theme : str):
        super().__init__()

        self.HR = HR
        self.register_name = register_name
        self.language = language
        self.theme = theme
        row_layout = QHBoxLayout()

        reg_type = "instruction_pointer" if register_name == "IP" else "functional_registers" 
        reg_color = colors[self.theme][reg_type]

        self.register_label = QLabel(register_name)
        self.register_label.setFont(bold_16)
        self.register_label.setStyleSheet(f'color: {reg_color};')
        self.register_label.setToolTip(color_txt(
                                        names[self.language][f"{self.register_name}_hint"],
                                        colors[theme]["hints"]))
        self.register_label.setFixedWidth(reg_label_width)
        self.register_label.setFixedHeight(register_height)

        self.register_content = QLineEdit()
        self.register_content.setFixedWidth(width_16_bit)
        self.register_content.setFixedHeight(register_height)
        self.register_content.setStyleSheet(register_text_style)
        self.register_content.setReadOnly(True)
        self.register_content.setAlignment(alg_cent)

        equals_label = QLabel("=")
        equals_label.setFixedHeight(register_height)

        self.register_decimal_value = QLineEdit()
        self.register_decimal_value.setFixedWidth(width_int)
        self.register_decimal_value.setFixedHeight(register_height)
        self.register_decimal_value.setReadOnly(True)
        self.register_decimal_value.setAlignment(alg_cent)

        row_layout.addWidget(self.register_label)
        row_layout.addWidget(self.register_content)
        row_layout.addWidget(equals_label)
        row_layout.addWidget(self.register_decimal_value)

        self.setLayout(row_layout)
        self.update()

    def _setRegisterValue(self, value : str):
        value = value.zfill(16)[-16:]
        self.register_content.setText(value)
        self.register_decimal_value.setText(f"{int(value, base=2)}")

    def update(self):
        self._setRegisterValue(self.HR.readFromRegister(self.register_name))

    def get_name(self):
        return self.register_name

    def set_interactive(self, value : bool = False):
        self.register_content.setReadOnly(not value)

    def set_hint(self, language : str):
        self.language = language
        name = f"{self.register_name}_hint"
        self.register_label.setToolTip(color_txt(
            names[self.language][name], colors[self.theme]["hints"]))

    def change_theme(self, theme : str):
        current_hint = self.register_label.toolTip()
        self.theme = theme
        self.register_label.setToolTip(color_txt(current_hint, colors[self.theme]["hints"]))


class CustomIndicator(QLabel):
    """SubClass of Flags"""
    
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
        if self.turnedOnState:  self.setOff()
        else:                   self.setOn()
        self.stateChanged.emit(self.turnedOnState)

    def setChecked(self, state):
        if bool(state): self.setOn()
        else:           self.setOff()

    def setModifiable(self, option):
        self.modifiable = bool(option)

    def mousePressEvent(self, event):
        if self.modifiable and event.button() == Qt.MouseButton.LeftButton:
            self.toggleState()
        super().mousePressEvent(event)


class Flags(QWidget):
    """
    This class is responsible for display of flag register = it containts a text
    field with source value, and below it, there are checkbox'es working like 
    indicators for all flags which are important for the user
    """

    def __init__(self, FR : FlagRegister, language : str, theme : str):
        super().__init__()
        
        self.FR = FR
        self.language = language
        self.theme = theme

        flags_section = QFormLayout()
        flags_title_row = QHBoxLayout()
        self.flag_indicators_row_1 = QHBoxLayout()
        self.flag_indicators_row_2 = QHBoxLayout()
        self.flag_indicators_row_3 = QHBoxLayout()
        
        self.register_label = QLabel(names[language]["flags"])
        self.register_label.setFont(bold_16)
        self.register_label.setStyleSheet(f'color: {colors[self.theme]["flags_section"]}')

        self.register_content = QLineEdit()
        self.register_content.setStyleSheet(register_text_style)
        self.register_content.setFixedWidth(180)
        self.register_content.setReadOnly(True)
        self.register_content.setAlignment(alg_cent)
        self.register_content.returnPressed.connect(self._validate_register_content)

        self.flags = ['Overflow',        'Direction', 'Interrupt',
                      'Trap',            'Sign',      'Zero',
                      'Auxiliary carry', 'Parity',    'Carry']

        for f in self.flags:
            attr_name = f"{f.lower().replace(' ', '_')}_flag"
            setattr(self, attr_name, CustomIndicator(f))
            obj = getattr(self, attr_name)
            obj.setToolTip(color_txt(names[language][attr_name], '#8F8F8F'))
            obj.stateChanged.connect(lambda _, flag=f: self._flag_indicator_clicked(flag))

        flags_title_row.addWidget(self.register_label)
        flags_title_row.addWidget(self.register_content)
        flags_title_row.insertSpacing(1,20)

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

        flags_section.addRow(flags_title_row)
        flags_section.addRow(self.flag_indicators_row_1)
        flags_section.addRow(self.flag_indicators_row_2)
        flags_section.addRow(self.flag_indicators_row_3)
        
        self.setLayout(flags_section)
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

    def _setRegisterValue(self, value : str):
        value = value.zfill(16)[-16:]
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
            show_custom_popup(self.language, {"popup" : "improper_flags_value"})
            source_value = self.FR.readFlags()
            self._setRegisterValue(source_value)
        else:
            adjusted_text = text.zfill(16)[-16:]
            self._setRegisterValue(adjusted_text)

    def setDisabled(self, value : bool):
        for attr_name in dir(self):
            if attr_name.endswith('_flag'):
                attr_value = getattr(self, attr_name)
                attr_value.setDisabled(value)
        self.register_content.setDisabled(value)
        self.register_label.setDisabled(False)

    def set_hint(self, language : str):
        for f in self.flags:
            attr_name = f"{f.lower().replace(' ', '_')}_flag"
            obj = getattr(self, attr_name)
            obj.setToolTip(color_txt(names[language][attr_name], colors[self.theme]["hints"]))


class LineNumberArea(QWidget):
    """SubClass of CodeEditor"""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.myeditor = editor

    def sizeHint(self):
        return self.myeditor._line_number_area_width(), 0

    def paintEvent(self, event):
        self.myeditor._lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    """This class is responsible for creation of code field, which allows for display of 
    custom text field, with numered lines, and option to highlight a certain line"""

    def __init__(self, language : str, theme : str):
        super().__init__()
        self.language = language
        self.theme = theme
        self.lineNumberArea = LineNumberArea(self)
        self.number_area_width = 0

        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.blockCountChanged.connect(self._updateLine_number_area_width)
        self.updateRequest.connect(self._updateLineNumberArea)

        self._updateLine_number_area_width()
        self.textCursor().movePosition(QTextCursor.MoveOperation.Start)

        self.highlighted_lines = []

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        left, top, height = cr.left(), cr.top(), cr.height()
        width = self.number_area_width
        self.lineNumberArea.setGeometry(QRect(left, top, width, height))

    def setHighlight(self, line_numbers : list | None,
                     background_color : str | None = "", 
                     text_color : str | None = ""
                     ):
        """
        Podświetla wybrane linie i przewija widok, aby podświetlona linia była na ekranie.
        """
        extraSelections = []

        if not line_numbers:
            self.highlighted_lines = line_numbers
            self.setExtraSelections(extraSelections)

        if not background_color:    background_color = colors[self.theme]["line_highlight"]
        if not text_color:  text_color = colors[self.theme]["code_text"]

        for line_number in line_numbers:
            if line_number <= 0:    continue
            cursor = QTextCursor(self.document().findBlockByLineNumber(line_number - 1))
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor(background_color))
            selection.format.setForeground(QColor(text_color))
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = cursor
            selection.cursor.clearSelection()

            extraSelections.append(selection)

        self.highlighted_lines = line_numbers
        self.setExtraSelections(extraSelections)

        if line_numbers:
            target_line = line_numbers[0]
            block = self.document().findBlockByLineNumber(target_line - 1)
            if block.isValid():
                cursor = QTextCursor(block)
                self.setTextCursor(cursor)
                self.ensureCursorVisible()

                scroll_bar = self.verticalScrollBar()
                scroll_position = line_number - 20
                scroll_bar.setValue(scroll_position)

            self.highlighted_lines = line_numbers
            self.setExtraSelections(extraSelections)

    def setText(self, text):
        self.setPlainText(text)
        self._line_number_area_width()
        self._updateLine_number_area_width()

    def setEditable(self, editable):
        self.setReadOnly(not editable)

    def _line_number_area_width(self):
        digits = len(str(self.blockCount()))
        width = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        self.number_area_width = width

    def _updateLine_number_area_width(self):
        self.setViewportMargins(self.number_area_width, 0, 0, 0)

    def _updateLineNumberArea(self, rect, dy):
        self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

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
                painter.drawText(0, int(top), self.lineNumberArea.width(), 
                                 height, Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


class StackTable(QTableWidget):
    """
    This class allows to display Stack as a table with option to easily change
    content
    """
    
    def __init__(self, data: DataSegment, language : str, theme : str):
        super().__init__()

        self.language = language
        self.theme = theme
        self.no_of_rows = 65536
        self.data = data
        self.data_copy = None

        self.setRowCount(self.no_of_rows)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(names[self.language]["segment_col"])
        self.setColumnWidth(2,1)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(True)
        self.setGridStyle(Qt.PenStyle.SolidLine)
        self.setStyleSheet(table_grid)
        
        self.cellChanged.connect(self.onCellChanged)

    def generate_table(self):
        fresh_data = self.data.data
        self.data_copy = fresh_data[:]

        self.cellChanged.disconnect()

        for row, address in enumerate(range(self.no_of_rows-1, -1, -1)):
            address_hex = hex(address)[2:].upper()
            value_int = self.data_copy[address]
            value_bin = bin(value_int)[2:].zfill(8)
            
            row_no = QTableWidgetItem(address_hex)
            row_no.setFont(bold_italic_15)

            self.setItem(row, 0, row_no)
            self.setItem(row, 1, QTableWidgetItem(value_bin))
            self.setItem(row, 2, QTableWidgetItem(str(value_int)))
        
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.cellChanged.connect(self.onCellChanged)

    def set_allow_change_content(self, allow = True):
        self.allow_change = allow
        if allow:
            self.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        else:
            self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def refresh_table(self):
        fresh_data = self.data.data
        self.cellChanged.disconnect()

        r,g,b,i = colors[self.theme]["change_highlight"]
        highlight_color = QColor(r,g,b,i)

        if self.data_copy != fresh_data:
            for row, address in enumerate(range(self.no_of_rows-1, -1, -1)):
                if self.data_copy[address] != fresh_data[address]:
                    value_int = fresh_data[address]
                    value_bin = bin(value_int)[2:].zfill(8)
                    self.setItem(row, 1, QTableWidgetItem(value_bin))
                    self.setItem(row, 2, QTableWidgetItem(str(value_int)))
                    self.data_copy[address] = fresh_data[address]
                    self._highlightChange(row, 1, highlight_color)
                    self._highlightChange(row, 2, highlight_color)

        self.cellChanged.connect(self.onCellChanged)

    def onCellChanged(self, row, column):
        self.blockSignals(True)
        item = self.item(row, column)
        value = item.text().strip()
        
        if not self.allow_change or not value:
            self._restorePreviousValue(row)
            self.blockSignals(False)
            return

        match column:
            case 0:
                show_custom_popup(self.language, {"popup" : "cannot_edit_address"})
                self._restorePreviousValue(row)
            case 1:
                if not all(c in '01' for c in value):
                    show_custom_popup(self.language, {"popup" : "invalid_binary_number"})
                    self._restorePreviousValue(row)
                else:
                    decimal_value = int(value, 2)
                    if decimal_value > 255 or decimal_value < 0:
                        show_custom_popup(self.language, {"popup" : "incorrect_decimal_value"})
                        self._restorePreviousValue(row)
                        return
                    self.setItem(row, 1, QTableWidgetItem(value.zfill(8)))
                    self.setItem(row, 2, QTableWidgetItem(str(decimal_value)))
                    self._highlightChange(row, 1)
                    self._highlightChange(row, 2)
            case 2:
                if not value.isdigit():
                    show_custom_popup(self.language, {"popup" : "incorrect_decimal_value"})
                    self._restorePreviousValue(row)
                else:
                    decimal_value = int(value)
                    if decimal_value > 255 or decimal_value < 0:
                        show_custom_popup(self.language, {"popup" : "incorrect_decimal_value"})
                        self._restorePreviousValue(row)
                        return
                    binary_value = bin(decimal_value)[2:].zfill(8)
                    self.setItem(row, 1, QTableWidgetItem(binary_value))
                    self._highlightChange(row, 1)
                    self._highlightChange(row, 2)

        self.blockSignals(False)

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.StandardKey.Copy):
            self._copySelectionToClipboard()
        else:
            super().keyPressEvent(event)

    def set_header(self, language : str):
        self.language = language
        self.setHorizontalHeaderLabels(names[self.language]["segment_col"])

    def _restorePreviousValue(self, row):
        value_int = self.data_copy[self.no_of_rows - row]
        value_bin = bin(value_int)[2:].zfill(8)

        address = hex(self.no_of_rows - 1 - row)[2:].upper()
        row_no = QTableWidgetItem(address)
        row_no.setFont(bold_italic_15)

        self.setItem(row, 0, row_no)
        self.setItem(row, 1, QTableWidgetItem(str(value_bin)))
        self.setItem(row, 2, QTableWidgetItem(str(value_int)))

    def _copySelectionToClipboard(self):
        selected_ranges = self.selectedRanges()
        if not selected_ranges: return

        copied_text = []
        
        for selection in selected_ranges:
            rows = []
            for row in range(selection.topRow(), selection.bottomRow() + 1):
                cols = []
                for col in range(selection.leftColumn(), selection.rightColumn() + 1):
                    item = self.item(row, col)
                    cols.append(item.text() if item else "")
                rows.append("\t".join(cols))
            copied_text.append("\n".join(rows))

        clipboard = QApplication.clipboard()
        clipboard.setText("\n".join(copied_text))

    def _highlightChange(self, row, column, color):
        item = self.item(row, column)
        if not item:    return

        default_color = self.palette().color(QPalette.ColorRole.Base)
        original_color = item.background().color()
        if not original_color.isValid() or original_color == QColor(0, 0, 0):  
            original_color = default_color  
        item.setBackground(color)

        QTimer.singleShot(500, lambda: self._resetCellColor(row, column, original_color))

    def _resetCellColor(self, row, column, color):
        self.blockSignals(True)
        item = self.item(row, column)
        if item:    item.setBackground(color)
        self.blockSignals(False)


class VariableTable(QTableWidget):
    """This class allows to display Stack as a table with option to easily change
    content"""
    def __init__(self, engine : Engine, language : str, theme : str):
        super().__init__()
        self.language = language
        self.theme = theme
        self.data = engine.DS
        self.data_copy = []
        self.engine = engine
        self.allow_change = False

        columns = names[self.language]["variables_col"]
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(True)
        self.setGridStyle(Qt.PenStyle.SolidLine)
        self.setStyleSheet(table_grid)

        self.cellChanged.connect(self.onCellChanged)

    def set_allow_change_content(self, allow = True):
        self.allow_change = allow
        if allow:
            self.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        else:
            self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def generate_table(self):
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
            test = Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
            var_name.setFlags(test)
            item_address = QTableWidgetItem(str(address))
            item_address.setFlags(test)
            item_size = QTableWidgetItem(str(size))
            item_size.setFlags(test)
            item_format =  QTableWidgetItem(format_str)
            item_format.setFlags(test)

            self.setItem(row, 0, var_name)
            self.setItem(row, 1, item_address)
            self.setItem(row, 2, item_size)
            self.setItem(row, 3, item_format)
            self.setItem(row, 4, QTableWidgetItem(binary_content))

            self.data_copy.append(content)
        
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.cellChanged.connect(self.onCellChanged)

    def refresh_table(self):
        
        self.cellChanged.disconnect()

        r,g,b,i = colors[self.theme]["change_highlight"]
        highlight_color = QColor(r,g,b,i)

        for row, var in enumerate(self.variables):
            variable = self.variables[var]
            address = variable['address']
            size = variable['size']
            content = self.data.get_data(address, size)

            if self.data_copy[row] != content:
                binary_content = " ".join([bin(c)[2:].zfill(8) for c in content])
                self.setItem(row, 4, QTableWidgetItem(binary_content))
                self._highlightChange(row, 4, highlight_color)
                self.data_copy[row] = content

        self.cellChanged.connect(self.onCellChanged)

    def onCellChanged(self, row, column):
        """Handle cell edits and enforce binary/decimal rules"""

        self.blockSignals(True)
        item = self.item(row, column)
        value = item.text().strip()
        
        if not self.allow_change or not value:
            self._restorePreviousValue(row)
            self.blockSignals(False)
            return

        match column:
            case 0:
                show_custom_popup(self.language, {"popup" : "cannot_edit_name"})
                self._restorePreviousValue(row)
            case 1:
                show_custom_popup(self.language, {"popup" : "cannot_edit_address"})
                self._restorePreviousValue(row)
            case 2:
                show_custom_popup(self.language, {"popup" : "cannot_edit_size"})
                self._restorePreviousValue(row)
            case 3:
                show_custom_popup(self.language, {"popup" : "cannot_edit_format"})
                self._restorePreviousValue(row)
            case 4:
                if not all(c in '01' for c in value):
                    show_custom_popup(self.language, {"popup" : "invalid_binary_number"})
                    self._restorePreviousValue(row)
                else:
                    length = (len(value)//8 + 1) * 8 if len(value)//8 < len(value)/8 else len(value)//8
                    self.setItem(row, 4, QTableWidgetItem(value.zfill(length)))
                    self._highlightChange(row, 4)

        self.blockSignals(False)

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.StandardKey.Copy):
            self._copySelectionToClipboard()
        else:
            super().keyPressEvent(event)

    def set_header(self, language : str):
        self.language = language
        self.setHorizontalHeaderLabels(names[self.language]["variables_col"])

    def _restorePreviousValue(self, row):
        content = self.data_copy[row]
        binary_content = " ".join([bin(c)[2:].zfill(8) for c in content])
        self.setItem(row, 4, QTableWidgetItem(binary_content))

    def _copySelectionToClipboard(self):
        selected_ranges = self.selectedRanges()
        if not selected_ranges: return

        copied_text = []
        
        for selection in selected_ranges:
            rows = []
            for row in range(selection.topRow(), selection.bottomRow() + 1):
                cols = []
                for col in range(selection.leftColumn(), selection.rightColumn() + 1):
                    item = self.item(row, col)
                    cols.append(item.text() if item else "")
                rows.append("\t".join(cols))
            copied_text.append("\n".join(rows))

        clipboard = QApplication.clipboard()
        clipboard.setText("\n".join(copied_text))

    def _highlightChange(self, row, column, color):
        item = self.item(row, column)
        if not item:    return

        default_color = self.palette().color(QPalette.ColorRole.Base)
        original_color = item.background().color()
        if not original_color.isValid() or original_color == QColor(0, 0, 0):  
            original_color = default_color  
        item.setBackground(color)

        QTimer.singleShot(500, lambda: self._resetCellColor(row, column, original_color))

    def _resetCellColor(self, row, column, color):
        self.blockSignals(True)
        item = self.item(row, column)
        if item:    item.setBackground(color)
        self.blockSignals(False)


class LimitedInputTextEdit(QTextEdit):
    """SubClass of Terminal"""
    
    inputFinished = pyqtSignal(str)

    def __init__(self, char_limit = 1000):
        super().__init__()
        self.char_limit = char_limit
        self.current_input = ""
        self.setUndoRedoEnabled(False)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

    def keyPressEvent(self, event: QKeyEvent):
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

    def reset_char_limit(self):     self.char_limit = 1000


class Terminal(QWidget):
    """This class represents terminal"""
    
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.terminal = LimitedInputTextEdit(20)  # Limit to 20 chars
        self.terminal.setFont(font_15)
        self.terminal.setMinimumHeight(100)

        self.terminal.inputFinished.connect(self.handle_input)

        layout.addWidget(self.terminal)
        self.setLayout(layout)

    def handle_input(self, user_input: str):
        """Handle input when user presses Enter."""
        print(f"User input: {user_input}")

    def write_char(self, char: int):
        """Write characters to terminal programmatically."""
        text = self.terminal.toPlainText()
        self.terminal.setPlainText(text + chr(char))
