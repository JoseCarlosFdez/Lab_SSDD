import uuid  # noqa: D100
from typing import Optional

import Ice

from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet

from . import RemoteTypes as rt  # noqa: D100, F401


class Factory(rt.Factory):
    """Implementation of the Factory interface."""

    def __init__(self) -> None:
        """Initialize the Factory with an empty registry of objects."""
        self._data: dict[str, rt.RTypePrx] = {}

    def get(
        self, typeName: rt.TypeName, identifier: Optional[str], current: Optional[Ice.Current]=None
    ) -> rt.RTypePrx:
        """Get or create a remote object based on the typeName and identifier."""
        if not identifier:
            identifier = str(uuid.uuid4())
        if identifier in self._data:
            return self._data[identifier]
        if current is None or current.adapter is None:
            raise RuntimeError("El adaptador de Ice no está disponible.")
        if typeName == rt.TypeName.RDict:
            obj = RemoteDict(identifier)
        elif typeName == rt.TypeName.RSet:
            obj = RemoteSet(identifier)
        elif typeName == rt.TypeName.RList:
            obj = RemoteList(identifier)
        else:
            raise rt.TypeError(f"Unknown type: {typeName}")
        proxy = current.adapter.addWithUUID(obj)
        if proxy is None:
            raise RuntimeError("Error al registrar el objeto remoto, el proxy es None.")
        proxy = rt.RTypePrx.checkedCast(proxy)
        if not proxy:
            raise RuntimeError("Error al hacer checkedCast del proxy.")
        self._data[identifier] = proxy
        return proxy
