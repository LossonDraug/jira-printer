import csv
import os
import sys
import traceback

import jinja2

from .card import Cards

STORY_TEMPLATE_FILE = "card_template.html.j2"
FEATURE_TEMPLATE_FILE = "feature_template.html.j2"
JIRA_PRINTER_DIR = "jira-printer"


def process_file(raw_jira_issues: str, name_to_save: str):
    try:
        cards = _read_cards(raw_jira_issues)
        _save_cards(name_to_save, _render_cards(cards.story_cards, STORY_TEMPLATE_FILE), "stories")
        _save_cards(name_to_save, _render_cards(cards.feature_cards, FEATURE_TEMPLATE_FILE), "epics")
    except ValueError:
        return "Please do not use filters while exporting Jira issues. Try again with a file containing all fields."
    except Exception as err:
        return "Unknown error occurred: " + traceback.format_exc()


def _save_cards(file_name: str, cards_stream, cards_type: str):
    with open(file_name + "_" + cards_type + ".html", "w") as f:
        f.write(cards_stream)


def _read_cards(file_name: str):
    with open(file_name, encoding='utf-8', errors='ignore') as jira_export_file:
        jira_export_csv = csv.reader(jira_export_file)
        jira_cards = Cards(next(jira_export_csv))
        for row in jira_export_csv:
            jira_cards.add_card(row)
    return jira_cards


def _render_cards(jira_cards: list, template: str):
    current_working_directory = os.getcwd()
    template_loader = jinja2.FileSystemLoader(searchpath=_relative_path("templates/"))
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template)
    return template.render(cards=jira_cards, path=_relative_path("icons/"))


def _relative_path(path):
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
