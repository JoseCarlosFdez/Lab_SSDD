class Iterable:  # noqa: D100
    """Implementation of the Iterable interface."""

    def __init__(self, data: list[str]) -> None:
        """Initialize the Iterable with a list of items."""
        self._data = data
        self._index = 0
        self._version = self._compute_version()

    def __iter__(self):
        """Return the iterator object itself (self)."""
        return self

    def __next__(self):
        """Return the next item from the iterator."""
        # Verifica si los datos han cambiado desde la última iteración
        if self._version != self._compute_version():
            raise StopIteration("The iterable was modified during iteration.")
        if self._index >= len(self._data):
            raise StopIteration()
        item = self._data[self._index]
        self._index += 1
        return item

    def reset(self):
        """Reset the iterator to the beginning of the data."""
        self._index = 0

    def _compute_version(self) -> int:
        """Compute a version hash for the current state of the data."""
        return hash(tuple(self._data))

    def update_data(self, new_data: list[str]) -> None:
        """Update the data of the iterable and reset the iterator."""
        self._data = new_data
        self._index = 0
        self._version = self._compute_version()  # Recalcular la versión
