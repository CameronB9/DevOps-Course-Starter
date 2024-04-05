from dotenv import load_dotenv, find_dotenv
from datetime import datetime

from todo_app.data.mongo_item import MongoItem
from todo_app.data.db import DB
from todo_app.data.get_trello_items import Trello

class MigrateTrelloData:

    def __init__(self) -> None:

        file_path = find_dotenv('.env')
        load_dotenv(file_path, override=True)

        self._db = DB()

    def _format_datetime(self, date: str):

        input_format = '%d/%m/%Y'
        output_format = '%Y-%m-%dT%H:%M:%S'
        date_obj = datetime.strptime(date, input_format)
        return date_obj.strftime(output_format)

    def _get_trello_items(self):
        return Trello().get_items()

    def _get_mongo_items(self):
        return [
            MongoItem(
                id = None,
                name = item.name,
                description=item.description,
                is_done=True if item.status == 'Completed' else False,
                due=self._format_datetime(item.due_date) if item.due_date is not None else None,
                modified_date=self._format_datetime(item.modified_date),
                mode = 'Save',
                trello_id=item.id
            )
                for item in self._get_trello_items()
        ]


    def _get_trello_ids(self):

        return [item.trello_id for item in self._get_mongo_items()]


    def _get_existing_ids(self):

        query = {
            'trello_id': { '$in': self._get_trello_ids() }
        }

        return [item.trello_id for item in self._db.get_items_filter(query)]


    def _get_items_to_insert(self):

        mongo_items = self._get_mongo_items()
        existing_ids = self._get_existing_ids()
        return [item for item in mongo_items if item.trello_id not in existing_ids]


    def insert_items(self):

        items_to_insert = self._get_items_to_insert()
        insert_len = len(items_to_insert)

        if insert_len > 0:
            inserted_ids = self._db.add_items(self._get_items_to_insert())
            print(f'Inserted {len(inserted_ids)} items from Trello')
        else:
            print('No new Trello items found')

if __name__ == "__main__":
    migration = MigrateTrelloData()
    migration.insert_items()
