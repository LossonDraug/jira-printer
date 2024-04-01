from PyQt5.QtWidgets import QWidget, QMessageBox

from jira_printer.gui_utils import get_icon
from jira_printer.path_utils import relative_path


class Info(QMessageBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.info_txt = open(relative_path("files/info.txt"), "r")
        self.width = 200
        self.height = 200
        self.init_ui()

    def init_ui(self):
        self.resize(200, 200)
        self.setIcon(QMessageBox.Information)
        self.setText("Jira Printer")
        self.setInformativeText(self.info_txt.readline()[2:])
        self.setDetailedText(self.info_txt.read())
        self.setWindowTitle("Info")
        self.setWindowIcon(get_icon("icons/info.png"))
        self.setStandardButtons(QMessageBox.Close)
