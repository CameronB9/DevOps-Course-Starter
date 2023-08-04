from todo_app.data.item import Item
from todo_app.view_models.index_view_model import ViewModel

from typing import List

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


status_test_params = [
    (
        [item for item in generate_mock_data()], 
        "What are you waiting for, there's 5 left!"
    ),
    (
        [item for item in generate_mock_data() if item.status == 'Completed'], 
        "Everything is complete, you can relax for now!"
    ),
    (
        [], 
        "Nothing here yet!"
    )
]

@pytest.mark.parametrize(
    "test_input, expected", 
    status_test_params
)
def test_status_messages_returns_the_correct_message(
    view_model: ViewModel, 
    test_input: List[Item], 
    expected: str
):
    view_model = ViewModel(test_input)

    status_message = view_model.item_status_message

    assert status_message == expected


checkbox_test_params = [
    (0, 'check_box_outline_blank'),
    (5, 'check_box')
]

@pytest.mark.parametrize('item_index, expected', checkbox_test_params)
def test_render_checkbox_icon_returns_the_correct_string(
    view_model: ViewModel, 
    item_index: int, 
    expected: str
):

    selected_item = view_model.items[item_index]
    result = view_model.render_checkbox_icon(selected_item)

    assert expected == result