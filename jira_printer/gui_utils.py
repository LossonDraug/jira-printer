from PyQt5.QtWidgets import QDesktopWidget


def center_window(widget):
    widget_frame = widget.frameGeometry()
    center_point = QDesktopWidget().availableGeometry().center()
    widget_frame.moveCenter(center_point)
    widget.move(widget_frame.topLeft())