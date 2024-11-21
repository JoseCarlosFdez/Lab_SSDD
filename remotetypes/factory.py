
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet


class Factory(rt.Factory):
    """Implementation of the Factory interface."""

    def __init__(self) -> None:
        self.objects = {}

    def get(self, typeName: rt.TypeName, identifier: str = None, current=None):
        """Return an instance of the requested type."""
        if identifier in self.objects:
            return self.objects[identifier]

        if typeName == rt.TypeName.RDict:
            obj = RemoteDict(identifier)
        elif typeName == rt.TypeName.RSet:
            obj = RemoteSet(identifier)
        elif typeName == rt.TypeName.RList:
            obj = RemoteList(identifier)
        else:
            raise rt.TypeError(f"Unknown type: {typeName}")

        adapter = current.adapter
        proxy = adapter.addWithUUID(obj)
        self.objects[identifier] = proxy
        return proxy
