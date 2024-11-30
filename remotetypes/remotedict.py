import json  # noqa: D100
import os
from typing import Optional
import Ice
from remotetypes import RemoteTypes as rt
from remotetypes.customdict import StringDict


class RemoteDict(rt.RDict):
    """Implementation of the RDict type with persistence."""

    def __init__(self, identifier: str, persist_file: str = "rdict.json") -> None:
        """Initialize the RemoteDict."""
        self._data = StringDict()
        self.id_ = identifier
        self._persist_file = persist_file
        self._load_from_file()

    def _load_from_file(self):
        """Load the dictionary data from the persistence file."""
        if os.path.exists(self._persist_file):
            with open(self._persist_file, "r") as f:
                data = json.load(f)
                self._data = StringDict(data.get(self.id_, {}))

    def _save_to_file(self):
        """Save the dictionary data to the persistence file."""
        if os.path.exists(self._persist_file):
            with open(self._persist_file, "r") as f:
                data = json.load(f)
        else:
            data = {}

        data[self.id_] = dict(self._data)
        with open(self._persist_file, "w") as f:
            json.dump(data, f)

    def setItem(self, key: str, item: str, current: Optional[Ice.Current] = None):
        """Set a key-value pair in the dictionary."""
        if not isinstance(key, str) or not isinstance(item, str):
            raise TypeError("Keys and values must be strings.")
        self._data[key] = item
        self._save_to_file()

    def getItem(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Retrieve the value for a given key."""
        try:
            return self._data[key]
        except KeyError:
            raise rt.KeyError(f"Key '{key}' not found.")

    def pop(self, key: str, current: Optional[Ice.Current] = None) -> str:  # noqa: D102
        if key not in self._data:
            raise rt.KeyError(f"Key '{key}' not found.")
        value = self._data.pop(key)
        self._save_to_file()

        return value

    def remove(self, key: str, current: Optional[Ice.Current] = None):
        """Remove a key-value pair from the dictionary."""
        if key not in self._data:
            raise rt.KeyError(f"Key '{key}' not found.")
        del self._data[key]
        self._save_to_file()

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of items in the dictionary."""
        return len(self._data)

    def contains(self, key: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if a key exists in the dictionary."""
        return key in self._data

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash based on the dictionary's state."""
        return hash(frozenset(self._data.items()))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Return an iterator for the dictionary keys."""
        if current is None or current.adapter is None:
            raise ValueError("El adaptador no está disponible.")
        iterable_servant = RemoteDictIterator(self._data)
        proxy = current.adapter.addWithUUID(iterable_servant)
        return rt.IterablePrx.checkedCast(proxy)


class RemoteDictIterator(rt.Iterable):
    """Iterator for RemoteDict."""

    def __init__(self, data: dict):  # noqa: D107
        self._data = list(data.items())
        self._index = 0

    def next(self, current: Optional[Ice.Current] = None) -> str:  # noqa: D102
        if self._index >= len(self._data):
            raise rt.StopIteration
        key, value = self._data[self._index]
        self._index += 1
        return f"{key}:{value}"
