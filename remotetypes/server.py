"""remotetypes server application."""

import logging
import json
import Ice
from . import RemoteTypes as rt
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
    def performOperation(self, jsonData, current=None):
        """Maneja las operaciones recibidas basadas en el JSON."""
        self.logger.info(f"Operación recibida: {jsonData}")
        
        try:
            # Decodificar el JSON
            request = json.loads(jsonData)
            if isinstance(request, dict):
                request = [request]  # Convertir en lista si es un solo objeto

            responses = []
            for operation in request:
                response = {"id": operation.get("id")}

                # Validar que las claves obligatorias estén presentes
                required_keys = {"id", "object_identifier", "object_type", "operation"}
                if not all(key in operation for key in required_keys):
                    response["status"] = "error"
                    response["error"] = "Formato inválido: faltan claves obligatorias."
                    responses.append(response)
                    continue

                # Obtener el tipo de operación
                object_type = operation["object_type"]
                object_identifier = operation["object_identifier"]

                try:
                    # Procesar según el tipo de objeto (RSet, RList, RDict)
                    if object_type == "RSet":
                        result = self.handle_rset_operation(operation)
                    elif object_type == "RList":
                        result = self.handle_rlist_operation(operation)
                    elif object_type == "RDict":
                        result = self.handle_rdict_operation(operation)
                    else:
                        raise ValueError(f"Tipo de objeto no soportado: {object_type}")

                    response["status"] = "ok"
                    if result is not None:
                        response["result"] = result
                except Exception as e:
                    response["status"] = "error"
                    response["error"] = str(e)

                responses.append(response)

            return json.dumps(responses)

        except json.JSONDecodeError as e:
            self.logger.error(f"Error al decodificar el mensaje JSON: {e}")
            return json.dumps([{"id": None, "status": "error", "error": "JSONDecodeError"}])

        except ValueError as e:
            self.logger.error(f"Error en el formato del mensaje: {e}")
            return json.dumps([{"id": None, "status": "error", "error": str(e)}])

    def handle_rset_operation(self, operation):
        """Procesar operaciones RSet."""
        try:
            # Llamar a 'get' con el tipo adecuado de enumeración
            object_identifier = operation.get("object_identifier")
            result = self.get_object(rt.TypeName.RSet, object_identifier)
            return result
        except Exception as e:
            self.logger.error(f"Error al manejar RSet: {e}")
            raise

    def handle_rlist_operation(self, operation):
        """Procesar operaciones RList."""
        try:
            # Llamar a 'get' con el tipo adecuado de enumeración
            object_identifier = operation.get("object_identifier")
            result = self.get_object(rt.TypeName.RList, object_identifier)
            return result
        except Exception as e:
            self.logger.error(f"Error al manejar RList: {e}")
            raise

    def handle_rdict_operation(self, operation):
        """Procesar operaciones RDict."""
        try:
            # Llamar a 'get' con el tipo adecuado de enumeración
            object_identifier = operation.get("object_identifier")
            result = self.get_object(rt.TypeName.RDict, object_identifier)
            return result
        except Exception as e:
            self.logger.error(f"Error al manejar RDict: {e}")
            raise

    def get_object(self, typeName, identifier):
        """Obtiene un objeto según el tipo y el identificador."""
        self.logger.info(f"Obteniendo objeto de tipo {typeName} con identificador {identifier}")
        
        # Aquí debería haber lógica real para recuperar el objeto dependiendo de la implementación
        # Por ejemplo, si estuviera conectado a una base de datos o a otro sistema de almacenamiento
        return {"type": str(typeName), "identifier": identifier}  # Ejemplo de respuesta ficticia

