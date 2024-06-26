from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QColor, QLinearGradient, QBrush, QFont
from PyQt5.QtCore import pyqtSignal, QObject, Qt

from jira_printer import info
from jira_printer.path_utils import get_relative_path
from jira_printer import constants as c


class Communicate(QObject):
    closeApp = pyqtSignal()


class About(QWidget):
    def __init__(self):
        super().__init__()
        self.c = None
        self.title = 'About'
        self.width = 480
        self.height = 380
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        self.initUI()

    def initUI(self):
        self.setFixedSize(self.width, self.height)
        self.c = Communicate()
        self.c.closeApp.connect(self.close)
        self.setWindowIcon(QIcon(get_relative_path(c.icon)))
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.setAutoFillBackground(True)
        gradient = QLinearGradient(0, 0, 0, 600)
        gradient.setColorAt(1.0, QColor("#008eff"))
        gradient.setColorAt(0.0, QColor("#8fe966"))
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        layout = QGridLayout()
        layout.setSpacing(10)

        label = QLabel(info.get_label(), self)
        font = QFont('Monospace')
        font.setStyleHint(QFont.TypeWriter)
        label.setFont(font)
        name = QLabel("Jira Printer v." + info.get_version(), self)
        moto = QLabel(info.get_moto(), self)
        try:
            copyright_label = QLabel(("© {}".format(info.get_author()) + " " + info.get_year()), self)
        except Exception:
            copyright_label = QLabel(("(c) {}".format(info.get_author()) + " " + info.get_year()), self)

        git_hub = QLabel("<a href=\"https://github.com/LossonDraug/jira-printer\">Jira Printer on GitHub</a>", self)
        git_hub.setOpenExternalLinks(True)

        main_layout = QVBoxLayout()

        main_layout.addWidget(label, alignment=Qt.AlignCenter)
        main_layout.addWidget(name, alignment=Qt.AlignCenter)
        main_layout.addWidget(moto, alignment=Qt.AlignCenter)
        main_layout.addWidget(copyright_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(git_hub, alignment=Qt.AlignCenter)
        main_layout.setAlignment(Qt.AlignCenter)

        self.setLayout(main_layout)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.c.closeApp.emit()
