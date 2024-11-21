import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error


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

    def next(self, current=None) -> str:
        """
        Return the next item in the iteration.

        Raises:
            rt.StopIteration: If there are no more items.
        """
        if self._index >= len(self._data):
            raise rt.StopIteration()
        item = self._data[self._index]
        self._index += 1
        return item
