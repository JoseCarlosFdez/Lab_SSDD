import json
import os
from typing import Optional
import Ice
from remotetypes import RemoteTypes as rt
from remotetypes.customlist import StringList

class RemoteList(rt.RList):
    """Implementation of the remote interface RList with persistence."""

    def __init__(self, identifier: str, persist_file: str = "rlist.json") -> None:
        """
        Initialize a RemoteList with an empty list.

        Args:
            identifier (str): A unique identifier for this list instance.
        """
        self._data = []
        self.id_ = identifier
        self._persist_file = persist_file
        self._load_from_file()

    def _load_from_file(self):
        """Load the list data from the persistence file."""
        if os.path.exists(self._persist_file):
            with open(self._persist_file, "r") as f:
                data = json.load(f)
                self._data = data.get(self.id_, [])

    def _save_to_file(self):
        """Save the list data to the persistence file."""
        if os.path.exists(self._persist_file):
            with open(self._persist_file, "r") as f:
                data = json.load(f)
        else:
            data = {}

        data[self.id_] = self._data
        with open(self._persist_file, "w") as f:
            json.dump(data, f)

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    def append(self, item: str, current: Optional[Ice.Current] = None):
        if not isinstance(item, str):
            raise TypeError("Items must be strings.")
        self._data.append(item)
        self._save_to_file()

    def remove(self, item: str, current: Optional[Ice.Current] = None):
        if item not in self._data:
            raise rt.KeyError(f"Item '{item}' not found.")
        self._data.remove(item)
        self._save_to_file()

    def getItem(self, index: int, current: Optional[Ice.Current] = None) -> str:
        try:
            return self._data[index]
        except IndexError:
            raise rt.KeyError(f"Index '{index}' out of range.")

    def length(self, current: Optional[Ice.Current] = None) -> int:
        return len(self._data)

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        return hash(tuple(self._data))

    def pop(self, current: Optional[Ice.Current] = None) -> str:
        if not self._data:
            raise rt.KeyError("List is empty.")
        item = self._data.pop()
        self._save_to_file()
        return item

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        if current is None or current.adapter is None:
            raise ValueError("Adapter is not available.")
        iterable_servant = RemoteListIterator(self._data)
        proxy = current.adapter.addWithUUID(iterable_servant)
        return rt.IterablePrx.checkedCast(proxy)

class RemoteListIterator(rt.Iterable):
    def __init__(self, data: list):
        self._data = data
        self._index = 0

    def next(self, current: Optional[Ice.Current] = None) -> str:
        if self._index >= len(self._data):
            raise rt.StopIteration
        item = self._data[self._index]
        self._index += 1
        return item