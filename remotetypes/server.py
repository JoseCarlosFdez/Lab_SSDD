"""remotetypes server application."""

import logging

import Ice

from remotetypes.factory import Factory


class Server(Ice.Application):
    """Ice.Application for the server."""

    def __init__(self) -> None:
        """Initialise the Server objects."""
        super().__init__()
        self.logger = logging.getLogger(__file__)

    def run(self, args: list[str]) -> int:
        """Execute the main server actions."""

        # Cargar propiedades de Ice desde el archivo de configuración
        properties = self.communicator().getProperties()
        self.logger.info(f"Properties: {properties}")

        # Crear el adaptador sin propiedades
        adapter = self.communicator().createObjectAdapter("remotetypes")

        # Añadir el servant al adaptador
        factory_servant = Factory()
        proxy = adapter.add(factory_servant, self.communicator().stringToIdentity("factory"))
        self.logger.info('Proxy: "%s"', proxy)

        # Activar el adaptador
        adapter.activate()
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0


