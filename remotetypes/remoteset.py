import json
import os
from typing import Optional
import Ice
from remotetypes import RemoteTypes as rt
from remotetypes.customset import StringSet


class RemoteSet(rt.RSet):
    """Implementation of the RSet type with persistence."""

    def __init__(self, identifier: str, persist_file: str = "rset.json") -> None:
        """Initialize the RemoteSet."""
        self._data = StringSet()
        self.id_ = identifier
        self._persist_file = persist_file
        self._load_from_file()

    def _load_from_file(self):
        """Load the set data from the persistence file."""
        if os.path.exists(self._persist_file):
            with open(self._persist_file, "r") as f:
                data = json.load(f)
                self._data = set(data.get(self.id_, []))

    def _save_to_file(self):
        """Save the set data to the persistence file."""
        if os.path.exists(self._persist_file):
            with open(self._persist_file, "r") as f:
                data = json.load(f)
        else:
            data = {}

        data[self.id_] = list(self._data)
        with open(self._persist_file, "w") as f:
            json.dump(data, f)

    def add(self, item: str, current: Optional[Ice.Current] = None):
        """Add an item to the set."""
        if not isinstance(item, str):
            raise TypeError("Items must be strings.")
        self._data.add(item)
        self._save_to_file()

    def remove(self, item: str, current: Optional[Ice.Current] = None):
        """Remove an item from the set."""
        try:
            self._data.remove(item)
            self._save_to_file()
        except KeyError:
            raise rt.KeyError(f"Item '{item}' not found.")

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the set contains an item."""
        return item in self._data

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of items in the set."""
        return len(self._data)

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash based on the set's state."""
        return hash(frozenset(self._data))

    def pop(self, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an arbitrary item from the set."""
        if len(self._data) == 0:
            raise rt.KeyError("The set is empty.")  # Lanza un KeyError si está vacío
        item = self._data.pop()
        self._save_to_file()
        return item

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Return an iterator for the set items."""
        if current is None or current.adapter is None:
            raise ValueError("The adapter is not available.")

        # Create a servant for the iterator
        iterable_servant = RemoteSetIterator(self._data)

        # Register the servant with the adapter
        proxy = current.adapter.addWithUUID(iterable_servant)

        # Return a proxy of the expected type
        return rt.IterablePrx.checkedCast(proxy)


class RemoteSetIterator(rt.Iterable):
    """Iterator for RemoteSet."""

    def __init__(self, data: set):
        self._data = list(data)  # Safe copy of the items
        self._index = 0

    def next(self, current: Optional[Ice.Current] = None) -> str:
        if self._index >= len(self._data):
            raise rt.StopIteration  # No arguments
        item = self._data[self._index]
        self._index += 1
        return item
