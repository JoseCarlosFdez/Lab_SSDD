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
        self._data = {}

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

        # Register the new object with Ice
        print(f"Creando objeto {typeName} con identificador {identifier}")
        proxy = current.adapter.addWithUUID(obj)
        proxy = rt.RTypePrx.checkedCast(proxy)
        if not proxy:
            raise RuntimeError("Error al registrar el objeto remoto.")
        self._data[identifier] = proxy
        print(f"Objeto registrado: {proxy}")

        return proxy
