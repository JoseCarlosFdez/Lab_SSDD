import json
from confluent_kafka import Consumer, Producer, KafkaError
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

class KafkaClient:
    def __init__(self, bootstrap_servers, input_topic, output_topic, group_id):
        self.bootstrap_servers = bootstrap_servers
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.group_id = group_id

    def process_message(self, message):
        try:
            request = json.loads(message)
            responses = []

            for operation in request:
                response = {"id": operation["id"]}
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

    def handle_rset_operation(self, operation):
        # Implementa la lógica para manejar operaciones en RSet
        return "Resultado de RSet"

    def handle_rlist_operation(self, operation):
        # Implementa la lógica para manejar operaciones en RList
        return "Resultado de RList"

    def handle_rdict_operation(self, operation):
        # Implementa la lógica para manejar operaciones en RDict
        return "Resultado de RDict"

    def consume_messages(self):
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

if __name__ == "__main__":
    if len(sys.argv) < 5:
        logging.error("Uso: python3 client.py <bootstrap_servers> <input_topic> <output_topic> <group_id>")
        sys.exit(1)

    bootstrap_servers = sys.argv[1]
    input_topic = sys.argv[2]
    output_topic = sys.argv[3]
    group_id = sys.argv[4]

    app = KafkaClient(bootstrap_servers, input_topic, output_topic, group_id)
    sys.exit(app.main()) 