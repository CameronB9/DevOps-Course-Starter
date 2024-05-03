from datetime import datetime, timedelta
from typing import List
import pytest

from todo_app.data.mongo_item import MongoItem
from todo_app.view_models.index_view_model import ViewModel


def generate_mock_data(items = 10, num_todo = 5, modified_today = 5):

    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days = 1)).strftime('%Y-%m-%d')

    mock_items = [
        {
            "_id": str(i),
            "name": f"Test Item {i + 1}",
            "description": f"Test Item {i + 1} Description",
            "is_done": False if i < num_todo else True,
            "modified_date": today if i < modified_today else str(yesterday),
            "due": None
        }
            for i in range(items)
    ]

    return [MongoItem.from_dict(item) for item in mock_items]

@pytest.fixture
def view_model() -> ViewModel:
    data = generate_mock_data()
    error = ""
    return ViewModel(data, error)

def test_completed_items_returns_the_correct_data(view_model: ViewModel):
    completed_items = view_model.completed_items

    assert len(completed_items) == 5
    assert False not in [item.is_done for item in completed_items]

def test_todo_items_returns_the_correct_data(view_model: ViewModel):
    todo_items = view_model.todo_items

    assert len(todo_items) == 5
    assert True not in [item.is_done for item in todo_items]

def test_item_lists_returns_the_correct_data(view_model: ViewModel):
    item_lists = view_model.item_lists

    assert len(item_lists) == 2


status_test_params = [
    (
        [item for item in generate_mock_data()], 
        "What are you waiting for, there's 5 left!"
    ),
    (
        [item for item in generate_mock_data() if item.is_done == True], 
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
    test_input: List[MongoItem], 
    expected: str
):
    view_model = ViewModel(test_input, "")

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

should_show_all_test_params = [
    (generate_mock_data(10, 7), True),
    (generate_mock_data(10, 2), False),
]

@pytest.mark.parametrize('mock_data, expected', should_show_all_test_params)
def test_should_show_all_done_items_returns_the_correct_bool(mock_data, expected):
    view_model = ViewModel(mock_data)
    result = view_model.should_show_all_done_items

    assert expected == result

def test_recent_done_items_returns_correct_result():
    mock_data = generate_mock_data(15, 5, 10)
    view_model = ViewModel(mock_data)
    assert len(view_model.recent_done_items) == 5

def test_older_done_items_returns_correct_result(view_model: ViewModel):
    assert len(view_model.older_done_items) == 5