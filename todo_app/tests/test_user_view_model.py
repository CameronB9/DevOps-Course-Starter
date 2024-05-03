import pytest

from todo_app.user import Roles, User
from todo_app.view_models.user_view_model import UserViewModel




role_test_params = [
    (User(1, 'User 1', Roles.admin), True),
    (User(2, 'User 2', Roles.writer), True),
    (User(3, 'User 3', Roles.reader), False),
]

@pytest.mark.parametrize('user, expected', role_test_params)
def test_write_permission(user: User, expected: bool):
    view_model = UserViewModel(user)
    assert view_model.has_write_permission == expected


admin_test_params = [
    (User(1, 'User 1', Roles.admin), True),
    (User(2, 'User 2', Roles.writer), False),
    (User(3, 'User 3', Roles.reader), False),
]

@pytest.mark.parametrize('user, expected', admin_test_params)
def test_admin_permission(user: User, expected: bool):
    view_model = UserViewModel(user)
    assert view_model.is_admin == expected