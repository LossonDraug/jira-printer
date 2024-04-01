from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox

from jira_printer.path_utils import get_relative_path


def center_window(widget):
    widget_frame = widget.frameGeometry()
    center_point = QDesktopWidget().availableGeometry().center()
    widget_frame.moveCenter(center_point)
    widget.move(widget_frame.topLeft())


def get_icon(icon_path):
    return QIcon(get_relative_path(icon_path))


def message_box(title: str, text: str, type, parent=None):
    box = QMessageBox(parent)
    box.setGeometry(0, 0, 100, 50)
    box.setIcon(type)
    box.setWindowTitle(title)
    box.setText(text)
    center_window(box)
    return box