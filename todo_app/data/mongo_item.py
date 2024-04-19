from datetime import datetime

class MongoItem:
    def __init__(self, id, name, description, is_done, due, modified_date, mode, trello_id) -> None:
        if id is not None:
            self._id: str = id
        if trello_id is not None:
            self.trello_id = trello_id
        self.name: str = name
        self.description: str = description
        self.is_done: bool = is_done
        self.modified_date: str = modified_date

        self.handle_due_date(mode, due)


    @classmethod
    def from_dict(cls, dict, mode = None):
        return cls(
            id = dict['_id'] if '_id' in dict else None, 
            name = dict['name'], 
            description = dict['description'] if 'description' in dict else None,
            is_done = dict['is_done'],
            due = dict['due_date'] if 'due_date' in dict else None, 
            modified_date = dict['modified_date'], 
            mode = mode,
            trello_id = dict['trello_id'] if 'trello_id' in dict else None
        )
    
    def handle_due_date(self, mode, due):
        if due == None:
            self.due_date = None
            return None
        raw_date_format = '%Y-%m-%dT%H:%M:%S'
        due_date_obj = datetime.strptime(due, raw_date_format)

        if mode == "Save":
            self.due_date = due_date_obj.strftime(raw_date_format)
        else:
            self.due_date =due_date_obj.strftime('%d/%m/%Y')
    
    def update_status(self):
        self.is_done = not self.is_done