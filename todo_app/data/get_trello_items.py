import requests
from datetime import datetime

from todo_app.utils import get_trello_credentials
from todo_app.data.trello_item import TrelloItem


class Trello:
    def __init__(self) -> None:
        trello_credentials = get_trello_credentials()
        self.todo_list = trello_credentials['todo_list']
        self.completed_list = trello_credentials['completed_list']
        self.base_url = 'https://api.trello.com/1'
        self.base_query = trello_credentials['secrets']
        self.board_id = trello_credentials['board_id']

    def get_items(self):
        query = self.base_query | {
            'cards': 'open'
        }
        path = f'boards/{self.board_id}/lists'
        response = requests.get(f'{self.base_url}/{path}', params=query).json()

        cards = [
            TrelloItem.from_trello_card(card, list)
                for list in response
                    for card in list['cards']
        ]
        return cards