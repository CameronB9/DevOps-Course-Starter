import requests
import json

from todo_app.utils import get_trello_credentials


class TrelloSetup:

    def __init__(self) -> None:
        trello_credentials = get_trello_credentials()
        self.base_url = 'https://api.trello.com/1'
        self.base_query = trello_credentials['secrets']
        self.board_id = None


    def create_board(self):
        query = self.base_query | {
            'name': 'Test Board',
            'defaultLists': 'false'
        }
        path = 'boards'
        response = requests.post(f'{self.base_url}/{path}', params=query)
        return response.json()['id']

    def create_list(self, name: str, board_id: str) -> str:
        query = self.base_query | {
            'name': name,
            'idBoard': board_id
        }

        path = 'lists'
        response = requests.post(f'{self.base_url}/{path}', params=query)
        return response.json()['id']

    def delete_board(self):
        path = f'boards/{self.board_id}'
        requests.delete(f'{self.base_url}/{path}', params=self.base_query)