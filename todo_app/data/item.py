class Item:
    def __init__(self, id, name, description, status = "To Do") -> None:
        self.id = id
        self.name = name
        self.description = description
        self.status = status

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], card['desc'], list['name'])