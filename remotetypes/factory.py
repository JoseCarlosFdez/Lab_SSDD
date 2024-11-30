import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet
import Ice
from typing import Optional
import uuid
class Factory(rt.Factory):
    """Implementation of the Factory interface."""

    def __init__(self) -> None:
        """Initialize the Factory with an empty registry of objects."""
        self._data: dict[str, rt.RTypePrx] = {}

    def get(self, typeName: rt.TypeName, identifier: Optional[str], current: Optional[Ice.Current] = None) -> rt.RTypePrx:
        """Get or create a remote object based on the typeName and identifier."""
        if not identifier:
            identifier = str(uuid.uuid4())

        # Check if the object already exists
        if identifier in self._data:
            return self._data[identifier]

        # Validate the adapter
        if current is None or current.adapter is None:
            raise RuntimeError("El adaptador de Ice no está disponible.")

        # Create a new object
        if typeName == rt.TypeName.RDict:
            obj = RemoteDict(identifier)
        elif typeName == rt.TypeName.RSet:
            obj = RemoteSet(identifier)
        elif typeName == rt.TypeName.RList:
            obj = RemoteList(identifier)
        else:
            raise rt.TypeError(f"Unknown type: {typeName}")

        # Register the object with UUID
        proxy = current.adapter.addWithUUID(obj)

        # Check if proxy is None immediately after addWithUUID
        if proxy is None:
            raise RuntimeError("Error al registrar el objeto remoto, el proxy es None.")

        # Ensure that the proxy is valid before attempting to cast
        proxy = rt.RTypePrx.checkedCast(proxy)

        # Handle invalid cast
        if not proxy:
            raise RuntimeError("Error al hacer checkedCast del proxy.")

        # Store the proxy in the registry
        self._data[identifier] = proxy
        return proxy

