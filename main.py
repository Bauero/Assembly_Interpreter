"""This is main file, which lanuches the app. It's there to allow later support for adding
CLI interface alongside GUI"""

import sys
from PyQt6.QtWidgets import QApplication
from program import *

def main():
    app = QApplication([])
    engine = Engine()
    code_handeler = CodeHandler(engine)
    window = MainWindow(code_handeler)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
