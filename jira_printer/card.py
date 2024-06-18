import pypandoc

COMPONENTS = "Components"

HEADERS_ENGLISH = ["Description", "Issue Type", "Issue key", "Priority", "Summary", "Status",
                  "Reporter", "Epic Link Summary", "Custom field (Story Points)",
                  "Custom field (Story point estimate)"]

HEADERS_GERMAN = ["Beschreibung", "Vorgangstyp", "Vorgangsschlüssel", "Priorität", "Zusammenfassung", "Status",
                  "Autor", "Epic Link Zusammenfassung", "Benutzerdefinierte Felder (Story Points)",
                  "Benutzerdefinierte Felder (Story Point-Schätzung)"]

LANGUAGE_TO_HEADERS = {"en": HEADERS_ENGLISH, "de": HEADERS_GERMAN}


class Cards:
    wanted_headers = {}
    components_header_indices = []
    story_cards = []
    feature_cards = []
    language = ""

    def __init__(self, headers: list):
        self.story_cards = []
        self.feature_cards = []
        # TODO add error handling
        for lang, lang_headers in LANGUAGE_TO_HEADERS.items():
            if lang_headers[0] in headers:
                self.language = lang
        for index, lang_header in enumerate(LANGUAGE_TO_HEADERS.get(self.language)):
            self.wanted_headers[HEADERS_ENGLISH[index]] = headers.index(lang_header)
        self.components_header_indices = [i for i, header in enumerate(headers) if header == COMPONENTS]

    def add_card(self, values: list):
        card = {}
        for header, index in self.wanted_headers.items():
            if header == "Description":
                card[header] = pypandoc.convert_text(values[index], to="html", format="jira")
            else:
                card[header] = values[index]
        card[COMPONENTS] = [values[index] for index in self.components_header_indices if values[index] != '']
        if values[self.wanted_headers["Issue Type"]] == "Epic":
            self.feature_cards.append(card)
        else:
            self.story_cards.append(card)
