import sys

from PyQt5.QtWidgets import QApplication

from .main_window import App


def main():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
