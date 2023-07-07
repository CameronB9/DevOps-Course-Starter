import requests
from typing import TypedDict

from todo_app.utils import get_trello_credentials


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
            {
                'id': card['id'],
                'title': card['name'],
                'status': list['name'],
                'status_id': list['id']
            }
                for list in response
                    for card in list['cards']
        ]

        return cards

    def get_item(self, id: str):
        query = self.base_query | {
        }

        path = f'cards/{id}'

        response = requests.get(f'{self.base_url}/{path}', params=query)
        print(response)

        return response.json()
    
    def add_item(self, title: str):
        query = self.base_query | {
            'idList': self.todo_list,
            'name': title
        }

        path = 'cards'
        requests.post(f'{self.base_url}/{path}', params=query)

    def update_item(self, id, item):
        query = self.base_query | item

        path = f'cards/{id}'

        requests.put(f'{self.base_url}/{path}', params=query)
