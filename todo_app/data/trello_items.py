import requests
from datetime import datetime

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

    # Get the list of todo items sorted by status, due_date
    def get_items_sorted(self):
        todo_items = self.get_items()
        date_format = '%d/%m/%Y'
        completed_todos = [item for item in todo_items if item.status == 'Completed']
        # lambda to sort todo item by date, if a date doesn't exist a default future date is used
        sort_by_date = lambda x: datetime.strptime('01/01/2100', date_format) if x.due_date is None else datetime.strptime(x.due_date, date_format)

        sorted_todo_items = sorted([item for item in todo_items if item.status != 'Completed'], key = sort_by_date, reverse=False)
        sorted_completed_items = sorted(completed_todos, key = sort_by_date, reverse=False)

        # combine the 2 sorted lists
        return sorted_todo_items + sorted_completed_items

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
