#########################	IMPORT NEEDED MODULES	  #########################

import sys
from PyQt6.QtWidgets import QApplication
from gui import MainWindow
from engine import Engine
from code_handler import CodeHandler

#########################	  LAUNCH WINDOW APP		  #########################

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
