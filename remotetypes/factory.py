import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet


class Factory(rt.Factory):
    """Implementation of the Factory interface."""

    def __init__(self) -> None:
        """
        Initialize the Factory with an empty registry of objects.
        """
        self.objects = {}

    def get(self, typeName: rt.TypeName, identifier: str = None, current=None):
        """
        Return an instance of the requested type.

        Args:
            typeName (rt.TypeName): The type of object to create or retrieve.
            identifier (str): A unique identifier for the object.
            current (Optional[Ice.Current]): The current Ice runtime context.

        Returns:
            Proxy: A proxy to the requested remote object.

        Raises:
            rt.TypeError: If the typeName is unknown.
            ValueError: If the identifier is not provided.
        """
        if identifier is None:
            raise ValueError("An identifier must be provided.")

        # Return the existing object if it exists
        if identifier in self.objects:
            return self.objects[identifier]

        # Create a new object based on the typeName
        if typeName == rt.TypeName.RDict:
            obj = RemoteDict(identifier)
        elif typeName == rt.TypeName.RSet:
            obj = RemoteSet(identifier)
        elif typeName == rt.TypeName.RList:
            obj = RemoteList(identifier)
        else:
            raise rt.TypeError(f"Unknown type: {typeName}")

        # Register the new object with Ice and store its proxy
        adapter = current.adapter
        proxy = adapter.addWithUUID(obj)
        self.objects[identifier] = proxy
        return proxy
