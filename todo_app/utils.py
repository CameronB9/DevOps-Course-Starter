from os import getenv
from typing import TypedDict

class Secrets(TypedDict):
    key: str
    token: str

class Credentials(TypedDict):
    secrets: Secrets
    board_id: str
    todo_list: str
    completed_list: str

def get_trello_credentials() -> Credentials:
    return {
        'secrets': {
            'key': getenv('TRELLO_API_KEY'),
            'token': getenv('TRELLO_SECRET')
        },
        'board_id': getenv('TRELLO_BOARD_ID'),
        'todo_list': getenv('TRELLO_TODO_LIST_ID'),
        'completed_list': getenv('TRELLO_COMPLETED_LIST_ID')
    }
    