Para la ejecución de la practica basta con activar el entorno virtual fuera de la carpeta. Una vez hecho esto accedemos a la carpeta principal y ejecutamos el Servidor con la instruccion "remotetypes --Ice.Config=config/remotetypes.config".

Con el servidor ejecutandose abrimos otra terminal y activamos el entorno virtual y a la carpeta principal y ejecutamos "docker-compose down", "docker-compose up -d" . Accedemos a la carpeta de "tests". Una vez aquí, podemos ejecutar el cliente con el siguiente comando "python3 client.py "localhost:9092" "input_topic" "output_topic" "my-group" <PROXY>" el cual hay que remplazar el PROXY por el que nos de el servidor. Hecho esto se ejecutará el cliente y comprobará que todo funciona bien.

En otra terminal accedemos a la carpeta en la que hemos instalado kafka y a la carpeta "bin" y ejecutamos los siguientes comandos: "./kafka-topics.sh --bootstrap-server localhost:9092 --create --topic input_topic --partitions 1 --replication-factor 1" para crear en topic y "./kafka-console-producer.sh --topic input_topic --bootstrap-server localhost:9092" para poder enviarle mensajes al cliente.

Una vez iniciados las tres terminales, podemos escribir los mensajes que deseemos en la terminal de kafka con la estructura correspondiente y el cliente lo recibira, se lo mandará al servidor y recibiremos una respuesta de este con el resultado.

Se recomienda utilizar estos mensajes para enviarles:
{"id": 1, "object_identifier": "obj1", "object_type": "RSet", "operation": "add", "args": {"value": "nuevo_elemento"}}
{"id": 2, "object_identifier": "obj2", "object_type": "RList", "operation": "add", "args": {"value": "nuevo_elemento"}}
{"id": 3, "object_identifier": "obj3", "object_type": "RDict", "operation": "add", "args": {"key": "clave_nueva", "value": "valor_nuevo"}}




