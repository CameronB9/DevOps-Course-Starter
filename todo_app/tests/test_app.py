from dotenv import load_dotenv, find_dotenv
import pytest
from os import getenv
from datetime import datetime
from typing import List, Dict

import mongomock
from flask.testing import FlaskClient
import pymongo


from todo_app import app

@pytest.fixture(scope='module')
def vcr_config():
    return {
        'filter_query_parameters': [
            ('key', 'API-KEY'),
            ('token', 'API-TOKEN')
        ]
    }

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

class MockData:
    def __init__(self) -> None:
        self.mongo_client = pymongo.MongoClient(getenv('MONGO_CONNECTION_STRING'))
        self.db = self.mongo_client[getenv('MONGO_DATABASE_NAME')]
        self.collection = self.db['todos']

    def insert_todos(self, count: int = 10) -> List[str]:
        data = [
            {
                'name': f'Todo Item {i+1}',
                'description': f'Item {i+1} Description',
                'is_done': False,
                'modified_date': datetime.now().isoformat(),
                'due_date': None
            }
            for i in range(count)
        ]
        inserted = self.collection.insert_many(data)

        return inserted.inserted_ids

    
    def get_item(self, query: Dict):
        return self.collection.find_one(query)

        

def test_index_page(client: FlaskClient):

    MockData().insert_todos(10)

    response = client.get('/')
    decoded_response = response.data.decode()

    assert 'To Do' in decoded_response
    assert 'Completed' in decoded_response

    for i in range(10):
        assert f'Todo Item {i+1}' in decoded_response


def test_add_todo(client: FlaskClient):

    task_name = 'TEST_ADD_TASK'
    mock_data = MockData()

    form_data = {
        'todo-name': task_name,
        'todo-description': '',
        'todo-due-date': ''
    }

    response = client.post('/todo/add', data = form_data)

    query = {
        'name': task_name
    }

    added_item = mock_data.get_item(query)
    assert added_item is not None
    assert response.status_code == 302

def test_update_todo(client: FlaskClient):

    mock_data = MockData()
    id = mock_data.insert_todos(1)[0]

    response = client.post(f'/todo/change-status/{str(id)}')

    query = {
        '_id': id
    }

    updated_item = mock_data.get_item(query)

    assert updated_item['is_done'] == True
    assert response.status_code == 302

def test_delete_todo(client: FlaskClient):
    mock_data = MockData()
    id = mock_data.insert_todos(1)[0]
    response = client.post(f'/todo/delete/{id}')

    query = {
        '_id': id
    }

    deleted_item = mock_data.get_item(query)

    assert deleted_item is None
    assert response.status_code == 302
