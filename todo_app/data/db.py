from os import getenv
from typing import List
from bson import ObjectId

import pymongo

from todo_app.data.mongo_item import MongoItem

# Define a custom sorting key function
def custom_sorting_key(doc):
    # If due_date is None, return a value that comes last in sorting
    if doc['due_date'] is None:
        return float('inf')  # A very large number
    else:
        return doc['due_date']

class DB:
    def __init__(self):
        self.client = pymongo.MongoClient(getenv('MONGO_CONNECTION_STRING'))
        self.db = self.client['todo-db']
        self.collection = self.db['todos']

    def get_items(self) -> List[MongoItem]:
        arr = []
        pipeline = [
            {
                "$addFields": {
                    "_due_date": {
                        "$cond": {
                            "if": { 
                                "$eq": [ 
                                    "$due_date", None 
                                ]
                            }, 
                            "then": "3000-01-01T00:00:00", 
                            "else": "$due_date" 
                        }
                    }
                }
            },
            {
                "$match": {
                    "_due_date": { 
                        "$exists": True 
                    }
                }
            },
            {
                "$sort": {
                    "_due_date": 1
                }
            },
        ]
        result = self.collection.aggregate(pipeline)

        for item in result:
            arr.append(MongoItem.from_dict(item))
        return arr


    def get_item(self, id: str) -> MongoItem:
        objectId = ObjectId(id)
        item = self.collection.find_one({ '_id': objectId })

        return MongoItem.from_dict(item, mode="Save")

    def add_item(self, item: MongoItem) -> str:
        inserted_item = self.collection.insert_one(item.__dict__)

        return inserted_item.inserted_id

    def update_item(self, item: MongoItem) -> None:
        filter = { '_id': item._id }
        new_values = { "$set": item.__dict__ }
        self.collection.update_one(filter, new_values)

    def delete_item(self, item: MongoItem) -> None:
        self.collection.delete_one({ '_id': item._id })

    

