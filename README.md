Para la ejecución de la practica basta con activar el entorno virtual fuera de la carpeta. Una vez hecho esto accedemos a la carpeta principal y ejecutamos el Servidor con la instruccion "remotetypes --Ice.Config=config/remotetypes.config".

Con el servidor ejecutandose abrimos otra terminal y activamos el entorno virtual y a la carpeta principal y ejecutamos "docker-compose up -d", "docker exec -it <ID-del-container> kafka-topics.sh --create --topic output_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1", "docker exec -it "Nombre-del-container" kafka-topics.sh --create --topic input_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1".

En otra terminal accedemos a la carpeta de "tests" con el entorno virtual activado. Una vez aquí, podemos ejecutar el cliente con el siguiente comando "python3 client.py "localhost:9092" "input_topic" "output_topic" "my-group" <PROXY>" el cual hay que remplazar el PROXY por el que nos de el servidor. Hecho esto se ejecutará el cliente y comprobará que todo funciona bien.

Una vez iniciado el cliente,accedemos a la carpeta test y ejecutamos el producer en la segunda terminal que hemos abierto con este comando "python producer.py localhost:9092 input_topic".

Esto hará que los mensajes que he creado en el producer se envien al cliente y los procese.
