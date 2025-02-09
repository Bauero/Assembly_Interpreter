"""This is main file, which lanuches the app. It's there to allow later support for adding
CLI interface alongside GUI"""

import sys
from PyQt6.QtWidgets import QApplication
from gui import MainWindow
from engine import Engine
from code_handler import CodeHandler

def processArgv():	...

def main():
    app = QApplication([])
    engine = Engine()
    code_handeler = CodeHandler(engine)
    window = MainWindow(code_handeler)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    if sys.argv:
        processArgv()
    main()
