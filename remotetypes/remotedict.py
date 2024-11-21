import json
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
import Ice  # noqa: F401; pylint: disable=import-error
from typing import Optional
from uuid import uuid4
from remotetypes.iterable import Iterable

class RemoteDict(rt.RDict):
    """Implementation of the RDict type."""

    def __init__(self, identifier: str = None, persist_file: str = "rdict.json"):
        """
        Initialize the RemoteDict.

        Args:
            identifier (str): Optional identifier for the dictionary.
            persist_file (str): File for persisting the dictionary data.
        """
        self._data = {}
        self._identifier = identifier
        self._persist_file = persist_file

        # Load existing data if identifier is provided
        if self._identifier:
            self._load_from_file()

    def setItem(self, key: str, item: str):
        """Set a key-value pair in the dictionary."""
        if not isinstance(key, str) or not isinstance(item, str):
            raise TypeError("Keys and values must be strings.")
        self._data[key] = item
        self._save_to_file()

    def getItem(self, key: str) -> str:
        """Retrieve the value for a given key."""
        try:
            return self._data[key]
        except KeyError:
            raise KeyError(f"Key '{key}' not found.")

    def pop(self, key: str) -> str:
        """Retrieve and remove the value for a given key."""
        try:
            value = self._data.pop(key)
            self._save_to_file()
            return value
        except KeyError:
            raise KeyError(f"Key '{key}' not found.")

    def remove(self, key: str):
        """Remove a key-value pair from the dictionary."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found.")
        del self._data[key]
        self._save_to_file()

    def length(self) -> int:
        """Return the number of items in the dictionary."""
        return len(self._data)

    def contains(self, key: str) -> bool:
        """Check if a key exists in the dictionary."""
        return key in self._data

    def hash(self) -> int:
        """Calculate a hash based on the dictionary's state."""
        return hash(frozenset(self._data.items()))

    def iter(self):
        """Return an iterator for the dictionary keys."""
        return RemoteDictIterator(self._data)

    def _save_to_file(self):
        """Persist the dictionary data to a file."""
        if not self._identifier:
            return  # Do not persist if no identifier is provided
        try:
            with open(self._persist_file, "r") as file:
                all_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            all_data = {}

        all_data[self._identifier] = self._data
        with open(self._persist_file, "w") as file:
            json.dump(all_data, file)

    def _load_from_file(self):
        """Load dictionary data from a file."""
        try:
            with open(self._persist_file, "r") as file:
                all_data = json.load(file)
            self._data = all_data.get(self._identifier, {})
        except (FileNotFoundError, json.JSONDecodeError):
            self._data = {}


class RemoteDictIterator(rt.Iterable):
    """Iterator for RemoteDict."""

    def __init__(self, data: dict):
        self._data = list(data.keys())
        self._index = 0

    def next(self) -> str:
        """Return the next key in the dictionary."""
        if self._index >= len(self._data):
            raise StopIteration("No more items in the iterator.")
        item = self._data[self._index]
        self._index += 1
        return item
    
    def iter(self, current=None) -> rt.IterablePrx:
    
        adapter = current.adapter
        iterable = Iterable(list(self._data.keys()))
        proxy = adapter.addWithUUID(iterable)
        return rt.IterablePrx.checkedCast(proxy)
