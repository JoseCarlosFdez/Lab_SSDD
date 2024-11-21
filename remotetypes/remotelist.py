"""Needed classes to implement and serve the RList type."""
import Ice
from typing import Optional
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error


class RemoteList(rt.RList):
    """Skelenton for the RList implementation."""
    def append(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Append an item to the list."""
        self._data.append(item)
