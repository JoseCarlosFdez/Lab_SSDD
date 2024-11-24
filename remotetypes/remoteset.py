from typing import Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.customset import StringSet
from remotetypes.iterable import Iterable


class RemoteSet(rt.RSet):
    """Implementation of the remote interface RSet."""

    def __init__(self, identifier: str) -> None:
        """
        Initialize a RemoteSet with an empty StringSet.

        Args:
            identifier (str): A unique identifier for this set instance.
        """
        self._storage_ = StringSet()
        self.id_ = identifier
        self._hash_value = self._compute_hash()

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """
        Remove an item from the StringSet if it exists, or raise a remote exception.

        Args:
            item (str): The string to remove.

        Raises:
            rt.KeyError: If the item is not found in the set.
        """
        try:
            self._storage_.remove(item)
            self._update_hash()
        except KeyError as error:
            raise rt.KeyError(f"Item not found: {item}") from error

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the StringSet."""
        return len(self._storage_)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the item exists in the StringSet."""
        return item in self._storage_

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the internal StringSet."""
        return self._hash_value

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """
        Create an Iterable proxy for iterating over the set items.

        Args:
            current (Optional[Ice.Current]): Current Ice runtime context.

        Returns:
            rt.IterablePrx: Proxy to the remote Iterable instance.
        """
        adapter = current.adapter
        iterable = Iterable(list(self._storage_))  # Convert the set to a list for ordered iteration.
        proxy = adapter.addWithUUID(iterable)
        return rt.IterablePrx.checkedCast(proxy)

    def add(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """
        Add a new string to the StringSet.

        Args:
            item (str): The string to add.
        """
        self._storage_.add(item)
        self._update_hash()

    def pop(self, current: Optional[Ice.Current] = None) -> str:
        """
        Remove and return an arbitrary element from the set.

        Returns:
            str: The removed element.

        Raises:
            rt.KeyError: If the set is empty.
        """
        try:
            item = self._storage_.pop()
            self._update_hash()
            return item
        except KeyError as exc:
            raise rt.KeyError("The set is empty") from exc

    def _compute_hash(self) -> int:
        """Compute a hash value for the current state of the set."""
        contents = list(self._storage_)
        contents.sort()  # Ensure a consistent ordering for hashing.
        return hash(tuple(contents))

    def _update_hash(self) -> None:
        """Update the stored hash value when the set is modified."""
        self._hash_value = self._compute_hash()
