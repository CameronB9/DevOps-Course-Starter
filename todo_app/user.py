from typing import List

from flask_login import UserMixin, current_user
from flask import redirect

class Roles:
    admin = 'admin'
    writer = 'writer'
    reader = 'reader'

    @staticmethod
    def list() -> List[str]:
        return [Roles.reader, Roles.writer, Roles.admin]

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
    def _check_permission(fn):


        def wrapper(*args, **kwargs):
            user: User = current_user
            if user and user.role != Roles.reader:
                return fn(*args, **kwargs)
            
            return redirect('/?e=PERMISSION_ERROR')
        wrapper.__name__ = fn.__name__
        return wrapper

    @staticmethod
    def check_permission(level):

        def wrapper(fn):

            def decorator(*args, **kwargs):
                user: User = current_user
                if user:
                    condition = user.role == Roles.admin if level == 'admin' else user.role != Roles.reader
                    if condition:
                        return fn(*args, **kwargs)
                
                return redirect('/?e=PERMISSION_ERROR')
            decorator.__name__ = fn.__name__
            return decorator

        return wrapper
