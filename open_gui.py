

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
    window.welcomeScreen.close()
    window.programScreen.show()
    window.variableSection.generate_table()
    window._set_active_state(False)
    window.nextLineButton.setFocus()
    window.programScreen.showMaximized()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
