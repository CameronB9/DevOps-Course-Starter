from typing import List

from todo_app.data.item import Item

class ItemLists:
    def __init__(self, name: str, items: List[Item]):
        self._name = name
        self._items = items

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def items(self) -> List[Item]:
        return self._items