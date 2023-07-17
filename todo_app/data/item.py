from datetime import datetime

class Item:
    def __init__(self, id, name, description, due_date, status = "To Do") -> None:
        self.id = id
        self.name = name
        self.description = description
        self.status = status
        self.due_date = datetime.strptime(due_date[0:10], '%Y-%m-%d').strftime('%d/%m/%Y') if due_date else None

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], card['desc'],card['due'], list['name'])