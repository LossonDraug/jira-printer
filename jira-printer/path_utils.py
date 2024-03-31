import os
import sys

JIRA_PRINTER_DIR = "jira-printer"


def relative_path(path):
    if os.path.isdir(JIRA_PRINTER_DIR):
        return _resource_path(os.path.join(JIRA_PRINTER_DIR, path))
    else:
        return _resource_path(path)


def _resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
