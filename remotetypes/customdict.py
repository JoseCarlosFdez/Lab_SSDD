

from typing import Optional, Any

class StringDict(dict):
    """
    A custom dictionary that enforces string keys and provides
    additional functionality like optional uppercase transformation.
    """

    def __init__(self, *args: tuple[Any], force_upper_case: Optional[bool] = False, **kwargs: Any) -> None:
        """
        Initialize the CustomDict.

        Args:
            force_upper_case (bool): Whether to convert all keys to uppercase.
        """
        self.upper_case = force_upper_case
        super().__init__(*args, **kwargs)

        # Validate all keys on initialization
        for key in self.keys():
            if not isinstance(key, str):
                raise ValueError(f"All keys must be of type str, but got {type(key).__name__}")
            if self.upper_case:
                self._convert_key_case(key)

    def _convert_key_case(self, key: str) -> str:
        """
        Helper function to convert a key to uppercase if the flag is set.

        Args:
            key (str): The key to process.

        Returns:
            str: The processed key.
        """
        if self.upper_case:
            return key.upper()
        return key

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set a key-value pair, enforcing string keys and applying case conversion.

        Args:
            key (Any): The key to set.
            value (Any): The value to set.
        """
        if not isinstance(key, str):
            raise ValueError(f"Key must be of type str, but got {type(key).__name__}")

        key = self._convert_key_case(key)
        super().__setitem__(key, value)

    def __getitem__(self, key: Any) -> Any:
        """
        Get the value associated with a key.

        Args:
            key (Any): The key to retrieve.

        Returns:
            Any: The value associated with the key.
        """
        if not isinstance(key, str):
            raise ValueError(f"Key must be of type str, but got {type(key).__name__}")

        key = self._convert_key_case(key)
        return super().__getitem__(key)

    def __contains__(self, key: Any) -> bool:
        """
        Check if a key is in the dictionary.

        Args:
            key (Any): The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        if not isinstance(key, str):
            raise ValueError(f"Key must be of type str, but got {type(key).__name__}")

        key = self._convert_key_case(key)
        return super().__contains__(key)

    def update(self, *args: tuple[Any], **kwargs: Any) -> None:
        """
        Update the dictionary with key-value pairs.

        Args:
            *args: Positional arguments for update.
            **kwargs: Keyword arguments for update.
        """
        for key, value in dict(*args, **kwargs).items():
            self[key] = value
