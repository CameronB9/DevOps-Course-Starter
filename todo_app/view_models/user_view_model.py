from todo_app.user import Roles, User

class UserViewModel:

    def __init__(self, user: User | None) -> None:
        self.user = user


    @property
    def role(self) -> str:
        if self.user:
            return self.user.role
        return Roles.reader

    @property
    def has_write_permission(self) -> bool:
        if self.user:
            return self.user.role != Roles.reader
        return False

    @property
    def is_admin(self) -> bool:
        if self.user:
            return self.user.role == Roles.admin
        return False