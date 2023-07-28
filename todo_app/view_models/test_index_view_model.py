from todo_app.data.item import Item
from todo_app.view_models.index_view_model import ViewModel

import pytest

def generate_mock_data():
    mock_items = [
        (
            f'{i + 1}', 
            f'Item {i + 1}', 
            f'Item {i + 1} Description', 
            None, 
            'To Do' if i < 5 else 'Completed'
        )
            for i in range(10)
    ]

    return [Item(*item) for item in mock_items]

@pytest.fixture
def view_model() -> ViewModel:
    data = generate_mock_data()
    return ViewModel(data)

def test_completed_items_returns_the_correct_data(view_model: ViewModel):
    completed_items = view_model.completed_items

    assert len(completed_items) == 5
    assert 'To do' not in [item.status for item in completed_items]

def test_todo_items_returns_the_correct_data(view_model: ViewModel):
    todo_items = view_model.todo_items

    assert len(todo_items) == 5
    assert 'Completed' not in [item.status for item in todo_items]

def test_item_lists_returns_the_correct_data(view_model: ViewModel):
    item_lists = view_model.item_lists

    assert len(item_lists) == 2
