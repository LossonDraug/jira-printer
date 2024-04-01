from PyQt5.QtWidgets import QWidget, QMessageBox

from jira_printer.gui_utils import get_icon
from jira_printer.path_utils import get_relative_path


class Info(QMessageBox):
    def __init__(self, parent, file):
        super().__init__(parent)
        self.info_txt = open(get_relative_path(file), "r")
        self.width = 300
        self.height = 400
        self.init_ui()

    def init_ui(self):
        self.resize(self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setIcon(QMessageBox.Information)
        self.setText("Jira Printer                                                                              ")
        self.setInformativeText(self.info_txt.readline()[2:])
        self.setDetailedText(self.info_txt.read())
        self.setWindowTitle("Info")
        self.setWindowIcon(get_icon("icons/info.png"))
        self.setStandardButtons(QMessageBox.Close)
