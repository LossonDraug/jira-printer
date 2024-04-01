import pypandoc

COMPONENTS = "Components"

WANTED_HEADERS = ["Issue Type", "Issue key", "Priority", "Summary", "Status",
                  "Reporter", "Description", "Epic Link Summary", "Custom field (Story Points)",
                  "Custom field (Story point estimate)"]


class Cards:
    wanted_headers = {}
    components_header_indices = []
    story_cards = []
    feature_cards = []

    def __init__(self, headers: list):
        self.story_cards = []
        self.feature_cards = []
        for header in WANTED_HEADERS:
            self.wanted_headers[header] = headers.index(header)
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


