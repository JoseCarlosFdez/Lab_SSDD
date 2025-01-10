import json
import sys
import logging
from confluent_kafka import Consumer, Producer, KafkaError
import Ice
from remotetypes import RemoteTypes as rt

logging.basicConfig(level=logging.INFO)

class KafkaClient:
    def __init__(self, bootstrap_servers, input_topic, output_topic, group_id, proxy):
        self.bootstrap_servers = bootstrap_servers
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.group_id = group_id
        self.proxy = proxy

        self.consumer = Consumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        })
        self.producer = Producer({'bootstrap.servers': self.bootstrap_servers})

        # Configurar el proxy de Ice
        self.communicator = Ice.initialize()
        base_proxy = self.communicator.stringToProxy(self.proxy)
        self.proxy = rt.FactoryPrx.checkedCast(base_proxy)

        if not self.proxy:
            error_msg = "No se pudo realizar el cast al tipo FactoryPrx."
            logging.error(error_msg)
            raise RuntimeError(error_msg)

        logging.info("Proxy configurado exitosamente.")

    def process_and_send(self, message):
        try:
            # Procesar el mensaje JSON
            operation = json.loads(message)
            logging.info(f"Operación recibida: {operation}")

            # Mapeo de tipo de objeto
            type_map = {
                "RSet": rt.TypeName.RSet,
                "RList": rt.TypeName.RList,
                "RDict": rt.TypeName.RDict
            }

            # Validar object_type
            object_type = operation["object_type"]
            if object_type not in type_map:
                raise ValueError(f"Tipo de objeto desconocido: {object_type}")

            # Obtener el tipo enumerado y el identificador
            type_name = type_map[object_type]
            identifier = operation.get("object_identifier")  # Puede ser None si no está definido

            # Llamar al servidor remoto a través del proxy
            proxy_result = self.proxy.get(type_name, identifier)

            # Convertir el resultado del proxy a un formato serializable
            result = {
                "proxy": str(proxy_result)  # Convertimos el objeto a cadena
            }

            logging.info(f"Respuesta del servidor: {result}")
            return json.dumps({"status": "ok", "result": result})
        except Exception as e:
            logging.error(f"Error al procesar el mensaje: {e}")
            return json.dumps({"status": "error", "error": str(e)})

    def consume_messages(self):
        self.consumer.subscribe([self.input_topic])
        logging.info("Cliente Kafka escuchando mensajes...")

        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logging.error(msg.error())
                    break

            logging.info(f"Mensaje recibido: {msg.value().decode('utf-8')}")

            # Procesar el mensaje y enviar la respuesta al tema output_topic
            response = self.process_and_send(msg.value().decode('utf-8'))
            self.producer.produce(self.output_topic, response.encode('utf-8'))
            self.producer.flush()
            logging.info(f"Respuesta enviada: {response}")
            
    def handle_rset_operation(self, operation):
        try:
            # Usar la enumeración definida en remotetypes.py
            return self.proxy.get(rt.TypeName.RSet, operation.get("object_identifier"))
        except Exception as e:
            logging.error(f"Error al manejar RSet: {e}")
            raise

    def handle_rlist_operation(self, operation):
        try:
            # Usar la enumeración definida en remotetypes.py
            return self.proxy.get(rt.TypeName.RList, operation.get("object_identifier"))
        except Exception as e:
            logging.error(f"Error al manejar RList: {e}")
            raise

    def handle_rdict_operation(self, operation):
        try:
            # Usar la enumeración definida en remotetypes.py
            return self.proxy.get(rt.TypeName.RDict, operation.get("object_identifier"))
        except Exception as e:
            logging.error(f"Error al manejar RDict: {e}")
            raise
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

    client = KafkaClient(bootstrap_servers, input_topic, output_topic, group_id, proxy)
    client.consume_messages()
