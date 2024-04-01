from PyQt5.QtCore import QThread, pyqtSignal

from jira_printer.cards_utils import process_file


class Worker(QThread):
    output = pyqtSignal(str)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.input_file = ""
        self.output_file = ""

    def process_cards(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.start()
        # output = process_file(input_file, output_file)

    def run(self):
        output = process_file(self.input_file, self.output_file)
        self.output.emit(output)

    def __del__(self):
        self.exiting = True
        self.wait()