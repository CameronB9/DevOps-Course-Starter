from os import getenv
from typing import List

import pymongo

from todo_app.user import User, Roles


class UserManagement:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(getenv('MONGO_CONNECTION_STRING'))
        self.db = self.client[getenv('MONGO_DATABASE_NAME')]
        self.collection = self.db['users']

    def get_users(self) -> List[User]:
        result = self.collection.find()

        return [
            User(item['id'], item['username'], item['role'])
                for item in result
        ]

    def get_user(self, id) -> User | None:
        result = self.collection.find_one({ 'id': str(id) })

        return User(result['id'], result['username'], result['role']) if result else None

    def add_user(self, id, username: str, role: str) -> User:
        self.collection.insert_one({
            'id': str(id),
            'username': username,
            'role': role
        })

        return User(id, username, Roles.reader)

    def update_user_role(self, id, role: str):
        self.collection.update_one({ 
            'id': id 
        },
        {
            '$set': {
                'role': role
            }
        })
