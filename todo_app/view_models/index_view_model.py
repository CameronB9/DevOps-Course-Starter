from typing import List
from todo_app.data.item import Item

class ViewModel:
    def __init__(self, items: List[Item]):
        self._items = items

    @property
    def items(self) -> List[Item]:
        return self._items
    
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
    
    def render_checkbox_icon(self, item: Item) -> str:
        if item.status == 'Completed':
            return 'check_box'
        else:
            return 'check_box_outline_blank'