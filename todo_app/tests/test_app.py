from dotenv import load_dotenv, find_dotenv
from flask.testing import FlaskClient
import pytest
import os
import requests

from todo_app import app

TRELLO_BASE_URL = 'https://api.trello.com/1'

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

class StubResponse:
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

    
def stub(url, params = {}):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')

    fake_response_data = None

    if url == f'{TRELLO_BASE_URL}/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'idList': '1',
            'cards': [
                {
                    'id': '456', 
                    'name': 'Test card', 
                    'desc': 'Test Desc',
                    'dateLastActivity': '2023-08-04',
                    'due': '2023-08-04'
                }
            ]
        }]
    elif url == f'{TRELLO_BASE_URL}/cards':
        fake_response_data = []
    elif url == f'{TRELLO_BASE_URL}/cards/abc':
        fake_response_data = { 'idList': '1' }
    
    if fake_response_data == None:
        raise Exception(f'Integration test did not expect URL {url}')

    return StubResponse(fake_response_data)


def test_index_page(monkeypatch, client: FlaskClient):
    monkeypatch.setattr(requests, 'get', stub)
    response = client.get('/')
    decoded_response = response.data.decode()
    assert 'Test card' in decoded_response
    assert 'Test Desc' in decoded_response
    assert '04/08/2023' in decoded_response

def test_add_todo(monkeypatch, client: FlaskClient):
    monkeypatch.setattr(requests, 'post', stub)

    form_data = {
        'todo-name': 'Task 1',
        'todo-description': '',
        'todo-due-date': ''
    }

    response = client.post('/todo/add', data = form_data)

    assert response.status_code == 302

def test_update_todo(monkeypatch, client: FlaskClient):
    monkeypatch.setattr(requests, 'put', stub)
    monkeypatch.setattr(requests, 'get', stub)

    response = client.post('/todo/change-status/abc')

    assert response.status_code == 302

def test_delete_todo(monkeypatch, client: FlaskClient):
    monkeypatch.setattr(requests, 'delete', stub)

    response = client.post('/todo/delete/abc')

    assert response.status_code == 302
