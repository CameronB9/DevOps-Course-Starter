from typing import List
from datetime import datetime

from todo_app.user import User, Roles
from todo_app.data.item_lists import ItemLists
from todo_app.data.mongo_item import MongoItem

class ViewModel:
    def __init__(
        self, 
        items: List[MongoItem], 
        error: str | None = "",
    ):
        self._items = items
        self.error = error


    @property
    def items(self) -> List[MongoItem]:
        return self._items

    @property
    def todo_items(self) -> List[MongoItem]:
        return [item for item in self.items if item.is_done == False]

    @property
    def completed_items(self) -> List[MongoItem]:
        return [item for item in self.items if item.is_done == True]

    @property
    def item_lists(self) -> List[ItemLists]:

        hidden_items = None
        completed_items = self.completed_items

        if self.should_show_all_done_items == False:
            completed_items = self.recent_done_items
            hidden_items = self.older_done_items
        return [
            ItemLists('To Do', self.todo_items), 
            ItemLists('Completed', completed_items, hidden_items)
        ]
    
    @property
    def num_items(self) -> int:
        return len(self.items)

    @property
    def num_completed_items(self) -> int:
        completed_items = [item for item in self.items if item.is_done == True]
        return len(completed_items)
    
    @property
    def item_status_message(self) -> str:
        if self.num_items == 0:
            return 'Nothing here yet!'
        elif self.num_completed_items == self.num_items:
            return 'Everything is complete, you can relax for now!'
        else:
            return f"What are you waiting for, there's {self.num_items - self.num_completed_items } left!"
    
    @property
    def should_show_all_done_items(self) -> bool:
        return True if self.num_completed_items < 5 else False

    @property
    def recent_done_items(self):
        today = datetime.date(datetime.now()).strftime('%Y-%m-%d')
        return [
            item 
                for item in self.completed_items if item.modified_date == today 
        ]

    @property
    def older_done_items(self):
        today = datetime.date(datetime.now()).strftime('%d/%m/%Y')
        return [item for item in self.completed_items if item.modified_date != today ]

    def render_error(self) -> str:
        if self.error == 'PERMISSION_ERROR':
            return ' You don\'t have permission to perform this action!'

        return ''

    def render_checkbox_icon(self, item: MongoItem) -> str:
        if item.is_done == True:
            return 'check_box'
        else:
            return 'check_box_outline_blank'