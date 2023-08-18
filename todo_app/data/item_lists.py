from typing import List

from todo_app.data.item import Item

class ItemLists:
    def __init__(self, name: str, items: List[Item], hidden_items: List[Item] = None):
        self._name = name
        self._items = items
        self._hidden_items = hidden_items

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def items(self) -> List[Item]:
        #return self._items
        items = [ItemList(self._items)]
        if self.hidden_items is not None:
            items.append(ItemList(self.hidden_items, True))

        return items
    
    @property
    def hidden_items(self) -> List[Item]:
        return self._hidden_items

class ItemList:
    def __init__(self, items: List[Item], is_hidden: bool = False) -> None:
        self._is_hidden = is_hidden
        self._items = items

    @property
    def is_hidden(self) -> bool:
        return self._is_hidden

    @property
    def items(self) -> List[Item]:
        return self._items