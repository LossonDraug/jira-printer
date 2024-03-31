import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QMessageBox, QMainWindow, QStatusBar, QAction

from . import about
from .cards_utils import process_file
from .path_utils import relative_path
from .gui_utils import center_window


WARNING = QMessageBox.Warning
CRITICAL = QMessageBox.Critical


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # global settings
        self.width = 600
        self.height = 400
        self.left = 10
        self.top = 10
        self.title = "Welcome to Jira Printer!"

        # elements to use globally
        self.central_widget = None
        self.opened_file_textbox = None
        self.save_file_textbox = None
        self.status_bar = None
        self.status = None
        self.about_window = about.About()

        # initiate UI
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # initialize global elements
        self.central_widget = QWidget()
        self.opened_file_textbox = self.read_only_textbox()
        self.save_file_textbox = self.read_only_textbox()
        self.status_bar = self.main_status_bar()

        # manage layouts
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.horizontal_widget(self.instruction_label()))
        main_layout.addWidget(self.horizontal_widget(self.open_file_button(), self.opened_file_textbox))
        main_layout.addWidget(self.horizontal_widget(self.name_to_save_file_button(), self.save_file_textbox))
        main_layout.addWidget(self.horizontal_widget(self.save_button()))
        main_layout.addWidget(self.horizontal_widget())
        self.central_widget.setLayout(main_layout)

        show_about = QAction(QIcon(relative_path("icons//info.png")), "&About", self)
        show_about.triggered.connect(self.about)

        info_menu = self.menuBar().addMenu("&About")
        info_menu.addAction(show_about)

        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready!")

        self.setCentralWidget(self.central_widget)
        center_window(self)
        self.setWindowIcon(QIcon(relative_path('icons/jira-printer-logo-transparent.png')))
        self.show()

    # Util functions

    def horizontal_widget(self, *args):
        horizontal_widget = QWidget(self)
        layout = QHBoxLayout()
        for widget in args:
            layout.addWidget(widget)
        horizontal_widget.setLayout(layout)
        return horizontal_widget

    def instruction_label(self):
        instructions = QLabel(self)
        instructions.setWordWrap(True)
        instructions.setGeometry(20, 20, 560, 200)
        instructions.setText("Please choose a csv file with exported Jira Issues you want to print. "
                             "Do not use label filtering.")
        return instructions

    # Buttons
    def open_file_button(self):
        button = QPushButton("Open", self)
        button.setToolTip("Choose a csv file with Jira Issues")
        button.clicked.connect(self.open_file_name_dialog)
        return button

    def name_to_save_file_button(self):
        button = QPushButton("Save as", self)
        button.setToolTip("Choose how to save the file")
        button.clicked.connect(self.save_file_dialog)
        return button

    def save_button(self):
        button = QPushButton("Process", self)
        button.setFixedHeight(50)
        button.setToolTip("Save the processed files")
        button.clicked.connect(self.process_and_save_file)
        return button

    # Text boxes
    def read_only_textbox(self):
        textbox = QLineEdit(self)
        textbox.setReadOnly(True)
        return textbox

    # Dialogs
    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose a file", "",
                                                   "CSV (*.csv)", options=options)
        if file_name:
            self.opened_file_textbox.setText(file_name)

    def save_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Cards", "",
                                                   "HTML Files (*.html)", options=options)
        if file_name:
            self.save_file_textbox.setText(file_name)

    # Popups
    def message_box(self, title: str, text: str, type):
        box = QMessageBox()
        box.setGeometry(0, 0, 100, 50)
        box.setIcon(type)
        box.setWindowTitle(title)
        box.setText(text)
        center_window(box)
        return box

    def about(self):
        center_window(self.about_window)
        self.about_window.show()

    # Status Bar Elements
    def main_status_bar(self):
        status_bar = QStatusBar()
        return status_bar

    # UI Logic
    def process_and_save_file(self):
        self.status_bar.showMessage("Working...")

        input_file = self.opened_file_textbox.text()
        output_file = self.save_file_textbox.text()

        if input_file == '':
            self.message_box("Warning", "No file to process!", WARNING).exec_()
            self.status_bar.showMessage("Aborted!")
        elif output_file == '':
            self.message_box("Warning", "No destination to save!", WARNING).exec_()
            self.status_bar.showMessage("Aborted!")
        else:
            outcome = process_file(input_file, output_file)
            self.status_bar.showMessage("Working...")
            if outcome:
                self.message_box("Critical", outcome, CRITICAL).exec_()
                self.status_bar.showMessage("Aborted!")
