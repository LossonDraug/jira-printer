import os
import sys

from PyQt5.QtWidgets import QApplication

from jira_printer.main_window import App


def main():
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "2"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "2"
    os.environ["QT_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
