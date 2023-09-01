from typing import List
from datetime import datetime

from todo_app.data.item import Item
from todo_app.data.item_lists import ItemLists

class ViewModel:
    def __init__(self, items: List[Item]):
        self._items = items

    @property
    def items(self) -> List[Item]:
        return self._items

    @property
    def todo_items(self) -> List[Item]:
        return [item for item in self.items if item.status == 'To Do']

    @property
    def completed_items(self) -> List[Item]:
        return [item for item in self.items if item.status == 'Completed']

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
        completed_items = [item for item in self.items if item.status == 'Completed']
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
        today = datetime.date(datetime.now()).strftime('%d/%m/%Y')
        return [item for item in self.completed_items if item.modified_date == today ]

    @property
    def older_done_items(self):
        today = datetime.date(datetime.now()).strftime('%d/%m/%Y')
        return [item for item in self.completed_items if item.modified_date != today ]

    def render_checkbox_icon(self, item: Item) -> str:
        if item.status == 'Completed':
            return 'check_box'
        else:
            return 'check_box_outline_blank'