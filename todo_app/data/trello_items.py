import requests
from typing import TypedDict

from todo_app.utils import get_trello_credentials
from todo_app.data.item import Item


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
            Item.from_trello_card(card, list)
                for list in response
                    for card in list['cards']
        ]
        return cards

    def get_item(self, id: str):
        path = f'cards/{id}'

        response = requests.get(f'{self.base_url}/{path}', params=self.base_query)
        print(response)

        return response.json()
    
    def add_item(self, to_add):
        query = self.base_query | to_add | {
            'idList': self.todo_list,
        }

        path = 'cards'
        requests.post(f'{self.base_url}/{path}', params=query)


    def update_item(self, id, item):
        query = self.base_query | item

        path = f'cards/{id}'

        requests.put(f'{self.base_url}/{path}', params=query)
    
    def delete_item(self, id):
        path = f'cards/{id}'

        requests.delete(f'{self.base_url}/{path}', params=self.base_query)
