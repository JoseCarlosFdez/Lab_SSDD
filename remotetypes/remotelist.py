from typing import Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error


class RemoteList(rt.RList):
    """Implementation of the remote interface RList."""

    def __init__(self, identifier: str) -> None:
        """
        Initialize a RemoteList with an empty list.

        Args:
            identifier (str): A unique identifier for this list instance.
        """
        self._storage = []
        self._identifier = identifier

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self._identifier

    def append(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """
        Add a string to the end of the list.

        Args:
            item (str): The string to add.

        Raises:
            rt.TypeError: If the item is not a string.
        """
        if not isinstance(item, str):
            raise rt.TypeError("Only string items are allowed in RemoteList.")
        self._storage.append(item)

    def pop(self, index: Optional[int] = None, current: Optional[Ice.Current] = None) -> str:
        """
        Remove and return the item at the given index, or the last item if no index is specified.

        Args:
            index (Optional[int]): The index of the item to remove.

        Returns:
            str: The removed item.

        Raises:
            rt.IndexError: If the index is out of bounds.
        """
        try:
            if index is None:
                return self._storage.pop()
            return self._storage.pop(index)
        except IndexError as e:
            raise rt.IndexError(f"Index out of range: {index}") from e

    def getItem(self, index: int, current: Optional[Ice.Current] = None) -> str:
        """
        Get the item at the specified index.

        Args:
            index (int): The index of the item.

        Returns:
            str: The item at the given index.

        Raises:
            rt.IndexError: If the index is out of bounds.
        """
        try:
            return self._storage[index]
        except IndexError as e:
            raise rt.IndexError(f"Index out of range: {index}") from e

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """
        Remove the first occurrence of the specified item from the list.

        Args:
            item (str): The item to remove.

        Raises:
            rt.KeyError: If the item is not found in the list.
        """
        try:
            self._storage.remove(item)
        except ValueError as e:
            raise rt.KeyError(f"Item not found: {item}") from e

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of items in the list."""
        return len(self._storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the item exists in the list."""
        return item in self._storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash for the list's current state."""
        return hash(tuple(self._storage))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """
        Return an Iterable proxy for iterating over the list items.

        Args:
            current (Optional[Ice.Current]): Current Ice runtime context.

        Returns:
            rt.IterablePrx: Proxy to the remote Iterable instance.
        """
        adapter = current.adapter
        iterable = Iterable(self._storage)
        proxy = adapter.addWithUUID(iterable)
        return rt.IterablePrx.checkedCast(proxy)
