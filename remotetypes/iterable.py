import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from typing import Optional
import Ice


class Iterable(rt.Iterable):
    """Implementation of the Iterable interface."""

    def __init__(self, data: list[str]) -> None:
        """
        Initialize the Iterable with a list of items.

        Args:
            data (list[str]): List of items to iterate over.
        """
        self._data = data
        self._index = 0
        self._version = self._compute_version()

    def next(self, current: Optional[Ice.Current] = None) -> str:
        """
        Return the next item in the iteration.

        Raises:
            rt.StopIteration: If there are no more items.
            rt.CancelIteration: If the underlying data is modified during iteration.
        """
        if self._version != self._compute_version():
            raise rt.CancelIteration("The iterable was modified during iteration.")

        if self._index >= len(self._data):
            raise rt.StopIteration()

        item = self._data[self._index]
        self._index += 1
        return item

    def reset(self, current: Optional[Ice.Current] = None) -> None:
        """
        Reset the iterator to the beginning of the data.

        Args:
            current (Optional[rt.Current]): Current Ice runtime context.
        """
        self._index = 0

    def _compute_version(self) -> int:
        """
        Compute a version hash for the current state of the data.

        Returns:
            int: A hash representing the current version of the data.
        """
        return hash(tuple(self._data))

    def update_data(self, new_data: list[str], current: Optional[Ice.Current] = None) -> None:
        """
        Update the data of the iterable and reset the iterator.

        Args:
            new_data (list[str]): The new list of items to iterate over.
            current (Optional[rt.Current]): Current Ice runtime context.
        """
        self._data = new_data
        self._index = 0
        self._version = self._compute_version()
