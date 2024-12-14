#!/usr/bin/env python3

import sys
import json
import logging
from typing import List, Dict, Any

from confluent_kafka import Consumer, Producer, KafkaError
import Ice
import remotetypes

logging.basicConfig(level=logging.INFO)

class KafkaClient(Ice.Application):
    def __init__(self, bootstrap_servers: str, input_topic: str, output_topic: str, group_id: str):
        super().__init__()
        self.bootstrap_servers = bootstrap_servers
        self.input_topic = input_topic
        self.output_topic = output_topic

        # Configurar Kafka Consumer
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
        })
        self.consumer.subscribe([input_topic])

        # Configurar Kafka Producer
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})

    def consume_messages(self):
        """Consume mensajes del topic de entrada y procesa cada mensaje."""
        try:
            while True:
                msg = self.consumer.poll(1.0)  # Espera un segundo para nuevos mensajes

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logging.error(f"Error en Kafka: {msg.error()}")
                        continue

                # Procesar mensaje válido
                self.process_message(msg.value().decode('utf-8'))
        finally:
            self.consumer.close()

    def process_message(self, message: str):
        """Procesa un mensaje recibido en formato JSON."""
        try:
            event = json.loads(message)

            if not isinstance(event, list):
                raise ValueError("El evento debe ser un array de operaciones.")

            responses = []
            for operation in event:
                response = self.handle_operation(operation)
                responses.append(response)

            # Enviar respuestas
            self.producer.produce(self.output_topic, json.dumps(responses).encode('utf-8'))
            self.producer.flush()

        except Exception as e:
            logging.error(f"Error al procesar mensaje: {e}")

    def handle_operation(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta una operación sobre un objeto remoto y devuelve la respuesta."""
        response = {"id": operation.get("id", "unknown"), "status": "error"}

        try:
            # Validar campos obligatorios
            required_keys = ["id", "object_identifier", "object_type", "operation"]
            if not all(key in operation for key in required_keys):
                raise ValueError("Faltan claves obligatorias en la operación.")

            object_type = operation["object_type"]
            object_id = operation["object_identifier"]
            op_name = operation["operation"]
            args = operation.get("args", {})

            # Manejar la operación iter
            if op_name == "iter":
                raise NotImplementedError("OperationNotSupported")

            # Obtener proxy del objeto remoto
            factory = self.get_factory()
            remote_object = self.get_remote_object(factory, object_type, object_id)

            # Ejecutar operación remota
            method = getattr(remote_object, op_name, None)
            if not method:
                raise AttributeError(f"Método {op_name} no soportado en {object_type}")

            result = method(**args) if args else method()
            response.update({"status": "ok", "result": result})

        except NotImplementedError as e:
            response.update({"error": "OperationNotSupported"})
        except Exception as e:
            response.update({"error": str(e)})

        return response

    def get_factory(self) -> remotetypes.RemoteTypes.FactoryPrx:
        """Obtiene la factoría remota usando el proxy del servidor."""
        proxy_str = "factory -t -e 1.1:tcp -h 192.168.100.104 -p 10000 -t 60000:tcp -h 172.21.0.1 -p 10000 -t 60000:tcp -h 172.17.0.1 -p 10000 -t 60000:tcp -h 172.18.0.1 -p 10000 -t 60000"
        proxy = self.communicator().stringToProxy(proxy_str)
        factory = remotetypes.RemoteTypes.FactoryPrx.checkedCast(proxy)
        if not factory:
            raise RuntimeError("El proxy proporcionado no es una factoría válida.")
        return factory

    def get_remote_object(self, factory, obj_type, identifier):
        """Obtiene un objeto remoto del tipo solicitado desde la factoría."""
        proxy = factory.get(obj_type, identifier)
        return proxy

    def run(self, args: List[str]) -> int:
        if len(args) < 5:
            logging.error("Uso: python3 client.py <bootstrap_servers> <input_topic> <output_topic> <group_id>")
            return 1

        bootstrap_servers = args[1]
        input_topic = args[2]
        output_topic = args[3]
        group_id = args[4]

        self.bootstrap_servers = bootstrap_servers
        self.input_topic = input_topic
        self.output_topic = output_topic

        try:
            self.consume_messages()
        except Exception as e:
            logging.error(f"Error durante la ejecución del cliente: {e}")
            return 1

        return 0

if __name__ == "__main__":
    app = KafkaClient()
    sys.exit(app.main(sys.argv))
