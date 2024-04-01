import ctypes
import sys
import webbrowser

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QMessageBox, QMainWindow, QStatusBar, QAction, QProgressBar, QSizePolicy, QTextEdit, QCheckBox

from jira_printer import about, info_window
from jira_printer.cards_utils import process_file
from jira_printer.path_utils import relative_path
from jira_printer.gui_utils import center_window, get_icon, message_box
from jira_printer import constants as c

WARNING = QMessageBox.Warning
CRITICAL = QMessageBox.Critical


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # global settings
        self.toolbar = None
        self.progress_bar = None
        self.width = 600
        self.height = 400
        self.left = 10
        self.top = 10
        self.title = "Welcome to Jira Printer!"

        # elements to use globally
        self.central_widget = None
        self.opened_file_textbox = None
        self.names_for_save = None
        self.status_bar = None
        self.status = None
        self.show_files_checkbox = None
        self.about_window = about.About()
        self.info_window = info_window.Info(self)
        self.save_as_name = ""

        # initiate UI
        self.init_ui()

    def init_ui(self):
        # make process distinguishable for windows in order to show app icon on a taskbar
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(c.my_app_id)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # initialize global elements
        self.central_widget = QWidget()
        self.opened_file_textbox = self.read_only_textbox()
        self.names_for_save = self.read_only_multiline_textbox(3)
        self.names_for_save.setText("Stores: \nEpics:")
        self.status_bar = self.main_status_bar()
        self.show_files_checkbox = QCheckBox(self)
        self.show_files_checkbox.setText("Open files after export")
        self.show_files_checkbox.setChecked(True)

        # manage layouts
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.horizontal_widget(self.instruction_label()))
        main_layout.addWidget(self.horizontal_widget(self.open_file_button(), self.opened_file_textbox))
        main_layout.addWidget(self.horizontal_widget(self.name_to_save_file_button(), self.names_for_save))
        main_layout.addWidget(self.horizontal_widget(self.show_files_checkbox))
        main_layout.addWidget(self.horizontal_widget(self.export_button()))
        main_layout.addWidget(self.horizontal_widget())
        self.central_widget.setLayout(main_layout)

        # Actions
        open_file = QAction(get_icon("icons/open.png"), "&Open File", self)
        open_file.triggered.connect(self.open_file_name_dialog)
        open_file.setStatusTip("Select file to process")

        save_as = QAction(get_icon("icons/save_as.png"), "&Name to save", self)
        save_as.triggered.connect(self.save_file_dialog)
        save_as.setStatusTip("Select the name for saving")

        export = QAction(get_icon("icons/export.png"), "&Export", self)
        export.triggered.connect(self.process_and_save_file)
        export.setStatusTip("Export Jira Cards")

        help_file = QAction(get_icon("icons/help.png"), "&Help", self)
        help_file.triggered.connect(lambda event: self.show_file(relative_path("files/Jira_Printer_help.pdf")))
        help_file.setStatusTip("I need help!")

        info = QAction(get_icon("icons/info.png"), "&Info", self)
        info.triggered.connect(self.show_info)
        info.setStatusTip("Show info and licenses")

        show_about = QAction(get_icon(c.icon), "&About", self)
        show_about.triggered.connect(self.about)
        show_about.setStatusTip("About this program")

        exit_action = QAction(get_icon("icons/exit.png"), "&Exit", self)
        exit_action.triggered.connect(sys.exit)
        exit_action.setStatusTip("Exit the program")

        # Menubar
        info_menu = self.menuBar().addMenu("&About")
        info_menu.addAction(help_file)
        info_menu.addAction(info)
        info_menu.addAction(show_about)

        # Toolbar
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.setIconSize(QSize(32, 32))
        self.toolbar.addAction(open_file)
        self.toolbar.addAction(save_as)
        self.toolbar.addAction(export)
        self.toolbar.addWidget(self.spacer())
        self.toolbar.addAction(help_file)
        self.toolbar.addAction(exit_action)

        # Statusbar
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready!")

        self.progress_bar = self.progress_bar_widget()
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.setHidden(True)

        self.setCentralWidget(self.central_widget)
        center_window(self)
        self.setWindowIcon(QIcon(relative_path(c.icon)))
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
                             "Use option \"Export CSV (all fields)\" in Jira.\n"
                             "If you have problems exporting Jira Issues open help file using button with \"?\" in the panel above.")
        return instructions

    # Buttons
    def open_file_button(self):
        button = QPushButton("Open", self)
        button.setToolTip("Choose a csv file with Jira Issues")
        button.clicked.connect(self.open_file_name_dialog)
        return button

    def name_to_save_file_button(self):
        button = QPushButton("Name to save", self)
        button.setToolTip("Choose how to save the file")
        button.clicked.connect(self.save_file_dialog)
        return button

    def export_button(self):
        button = QPushButton("Export", self)
        button.setFixedHeight(50)
        button.setToolTip("Save the processed files")
        button.clicked.connect(self.process_and_save_file)
        return button

    # Text boxes
    def read_only_textbox(self):
        textbox = QLineEdit(self)
        textbox.setReadOnly(True)
        return textbox

    def read_only_multiline_textbox(self, rows: int):
        textbox = QTextEdit(self)
        textbox.setFixedHeight(textbox.fontMetrics().lineSpacing() * rows)
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
            self.save_as_name = file_name
            self.names_for_save.setText("Stories: " + self.process_name(file_name, "stories") + "\n"
                                        + "Epics:    " + self.process_name(file_name, "epics"))

    # Popups
    def about(self):
        center_window(self.about_window)
        self.about_window.show()

    def show_info(self):
        center_window(self.info_window)
        self.info_window.show()

    # Status Bar and Tool Bar Elements
    def main_status_bar(self):
        status_bar = QStatusBar()
        return status_bar

    def progress_bar_widget(self):
        pbar = QProgressBar()
        pbar.setMinimum(0)
        pbar.setMaximum(0)
        pbar.setValue(0)
        return pbar

    def spacer(self):
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return spacer

    # UI Logic
    def process_and_save_file(self):
        self.status_bar.showMessage("Working...")
        self.progress_bar.setHidden(False)

        input_file = self.opened_file_textbox.text()
        output_file = self.save_as_name

        if input_file == '':
            message_box("Warning", "No file to process!", WARNING).exec_()
            self.status_bar.showMessage("Aborted!")
            self.progress_bar.setHidden(True)
        elif output_file == '':
            message_box("Warning", "No destination to save!", WARNING).exec_()
            self.status_bar.showMessage("Aborted!")
            self.progress_bar.setHidden(True)
        else:
            outcome = process_file(input_file, output_file)
            self.status_bar.showMessage("Saved!")
            self.progress_bar.setHidden(True)
            if self.show_files_checkbox.isChecked():
                self.show_file(self.process_name(self.save_as_name, "stories"))
                self.show_file(self.process_name(self.save_as_name, "epics"))
            if outcome:
                message_box("Critical", outcome, CRITICAL).exec_()
                self.status_bar.showMessage("Aborted!")
                self.progress_bar.setHidden(True)

    def show_file(self, url):
        new = 2
        path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
        if not webbrowser.get(path).open(url, new=new):
            path = "C:/Program Files/internet explorer/iexplore.exe %s"
            if not webbrowser.get(path).open(url, new=new):
                message_box("Error", "Unknown Error has occurred. The program cannot show the file in Webbrowser."
                                     "Please, open the corresponding file manually.", CRITICAL)

    def process_name(self, path: str, suffix: str):
        return path.replace(".html", '') + "_" + suffix + ".html"
