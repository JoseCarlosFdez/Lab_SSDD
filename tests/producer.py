from confluent_kafka import Producer
import logging
import sys
import json

logging.basicConfig(level=logging.DEBUG)

class KafkaProducer:
    def __init__(self, bootstrap_servers, output_topic):
        self.bootstrap_servers = bootstrap_servers
        self.output_topic = output_topic

        # Crear un productor Kafka
        self.producer = Producer({'bootstrap.servers': self.bootstrap_servers})

    def delivery_report(self, err, msg):
        """Muestra el estado de la entrega del mensaje"""
        if err is not None:
            logging.error(f"Error al enviar el mensaje: {err} para el mensaje: {msg.value()}")
        else:
            logging.info(f"Mensaje enviado a {msg.topic()} [{msg.partition()}]")


    def produce_message(self, message):
        """Envía un mensaje al tema de Kafka"""
        logging.debug(f"Enviando mensaje: {message}")
        # Convierte el diccionario a un string JSON y luego lo codifica en UTF-8
        message_json = json.dumps(message)
        self.producer.produce(self.output_topic, message_json.encode('utf-8'), callback=self.delivery_report)
        logging.debug("Mensaje enviado. Esperando respuesta...")
        self.producer.flush()
        logging.debug("Flush completado.")

    def main(self):
        # Mensaje que quieres enviar
        message = {"id": "1", "object_identifier": "obj1", "object_type": "RList", "operation": "add", "args": {"value": 5}}

        self.produce_message(message)
        message = {"id": "1", "object_identifier": "obj1", "object_type": "RDict", "operation": "add", "args": {"value": 5}}

        self.produce_message(message)
        message = {"id": "1", "object_identifier": "obj1", "object_type": "RSet", "operation": "add", "args": {"value": 5}}

        self.produce_message(message)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Uso: python producer.py <bootstrap_servers> <output_topic>")
        sys.exit(1)

    bootstrap_servers = sys.argv[1]
    output_topic = sys.argv[2]

    producer = KafkaProducer(bootstrap_servers, output_topic)
    producer.main()
