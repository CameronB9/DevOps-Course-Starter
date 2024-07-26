from typing import List
from functools import wraps
from flask import Flask

from flask_login import UserMixin, current_user
from flask import redirect

from todo_app.logger_config import LogAction, get_logger

class Roles:
    admin = 'admin'
    writer = 'writer'
    reader = 'reader'

    @staticmethod
    def list() -> List[str]:
        return [Roles.reader, Roles.writer, Roles.admin]

class Actions:
    add_todo = 'ADD_TODO'
    delete_todo = 'DELETE_TODO'
    update_status = 'UPDATE_TODO_STATUS'
    view_users = 'VIEW_USERS'
    update_user_role = 'UPDATE_USER_ROLE'


class User(UserMixin):
    def __init__(
        self, 
        id, 
        username = None,
        role: str = None
    ) -> None:
        super().__init__()
        self.id = id
        self.username = username
        self._role = role

    @property
    def role(self):
        return self._role if self._role is not None else Roles.reader

    @staticmethod
    def check_permission(level, action: Actions):
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                logger = get_logger()
                user: User = current_user
                if user:
                    condition = user.role == Roles.admin if level == 'admin' else user.role != Roles.reader
                    if condition:
                        return fn(*args, **kwargs)

                logger.info({
                    'message': f'user does not have permission to perform action',
                    "user_id": user.id,
                    "user_role": user.role,
                    "action": action,
                    "action_type": LogAction.permission
                })

                return redirect('/?e=PERMISSION_ERROR')
            return decorator

        return wrapper
