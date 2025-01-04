import json
from confluent_kafka import Consumer, Producer, KafkaError
import sys
import logging
import Ice
from remotetypes import RemoteTypes as rt

logging.basicConfig(level=logging.DEBUG)

class KafkaClient:
    def __init__(self, bootstrap_servers, input_topic, output_topic, group_id, proxy):
        self.bootstrap_servers = bootstrap_servers
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.group_id = group_id
        self.proxy = proxy

        self.communicator = Ice.initialize()

    def setup_proxy(self):
        base_proxy = self.communicator.stringToProxy(self.proxy)
        self.proxy = rt.FactoryPrx.checkedCast(base_proxy)

        if not self.proxy:
            error_msg = "No se pudo realizar el cast al tipo FactoryPrx."
            logging.error(error_msg)
            raise RuntimeError(error_msg)

        logging.info("Proxy configurado exitosamente.")

    def process_message(self, message):
        try:
            request = json.loads(message)  # Decodificar JSON

            if isinstance(request, dict):
                # Si el mensaje es un objeto, lo convertimos en un array con un único elemento
                request = [request]
            elif not isinstance(request, list):
                raise ValueError("El mensaje debe ser un array de operaciones o un único objeto.")

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

                try:
                    # Aquí puedes definir cómo manejar cada tipo de operación
                    if operation["object_type"] == "RSet":
                        result = self.handle_rset_operation(operation)
                    elif operation["object_type"] == "RList":
                        result = self.handle_rlist_operation(operation)
                    elif operation["object_type"] == "RDict":
                        result = self.handle_rdict_operation(operation)
                    else:
                        raise ValueError("Tipo de objeto no soportado")

                    response["status"] = "ok"
                    if result is not None:
                        response["result"] = result
                except Exception as e:
                    response["status"] = "error"
                    response["error"] = str(e)

                responses.append(response)

            return json.dumps(responses)
        except json.JSONDecodeError as e:
            logging.error(f"Error al decodificar el mensaje JSON: {e}")
            return json.dumps([{"id": None, "status": "error", "error": "JSONDecodeError"}])
        except ValueError as e:
            logging.error(f"Error en el formato del mensaje: {e}")
            return json.dumps([{"id": None, "status": "error", "error": str(e)}])

    def handle_rset_operation(self, operation):
        try:
            # Llamar al método remoto específico para RSet
            return self.proxy.performOperation(json.dumps(operation))
        except Exception as e:
            logging.error(f"Error al manejar RSet: {e}")
            raise

    def handle_rlist_operation(self, operation):
        try:
            # Llamar al método remoto específico para RList
            return self.proxy.performOperation(json.dumps(operation))
        except Exception as e:
            logging.error(f"Error al manejar RList: {e}")
            raise

    def handle_rdict_operation(self, operation):
        try:
            # Llamar al método remoto específico para RDict
            return self.proxy.performOperation(json.dumps(operation))
        except Exception as e:
            logging.error(f"Error al manejar RDict: {e}")
            raise

    def consume_messages(self):
        self.setup_proxy()
        consumer = Consumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        })
        consumer.subscribe([self.input_topic])

        producer = Producer({'bootstrap.servers': self.bootstrap_servers})

        logging.debug("Iniciando la consumición de mensajes...")
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                logging.debug("No se recibieron mensajes en esta iteración.")
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logging.debug("Fin de la partición alcanzado.")
                    continue
                else:
                    logging.error(msg.error())
                    break

            logging.info(f"Mensaje recibido: {msg.value().decode('utf-8')}")
            
            # Procesar el mensaje
            processed_message = self.process_message(msg.value().decode('utf-8'))
            producer.produce(self.output_topic, processed_message.encode('utf-8'))
            producer.flush()
            logging.debug(f"Mensaje procesado y enviado: {processed_message}")


    def main(self):
        try:
            self.consume_messages()
        except Exception as e:
            logging.error(f"Error durante la ejecución del cliente: {e}")
            return 1

        return 0

    def __del__(self):
        if self.communicator:
            self.communicator.destroy()

if __name__ == "__main__":
    if len(sys.argv) < 6:
        logging.error("Uso: python3 client.py <bootstrap_servers> <input_topic> <output_topic> <group_id> <proxy>")
        sys.exit(1)

    bootstrap_servers = sys.argv[1]
    input_topic = sys.argv[2]
    output_topic = sys.argv[3]
    group_id = sys.argv[4]
    proxy = sys.argv[5]
    app = KafkaClient(bootstrap_servers, input_topic, output_topic, group_id, proxy)
    sys.exit(app.main())