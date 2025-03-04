"""This is main file, which lanuches the app. It's there to allow later support for adding
CLI interface alongside GUI"""

import sys
from PyQt6.QtWidgets import QApplication
from program_code import *

def main():
    language = "PL"
    theme = "dark_mode"
    app = QApplication([])
    engine = Engine(language)
    code_handeler = CodeHandler(engine, language)
    window = MainWindow(code_handeler, language, theme)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
