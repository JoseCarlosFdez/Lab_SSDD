# Usar una imagen base de Python
FROM python:3.10-slim

# Instalar las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    libbz2-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Configurar el entorno de trabajo
WORKDIR /app
COPY . .

# Instalar las dependencias de Python
RUN pip install -r requirements.txt

# Comando para ejecutar tu aplicación (ajustar según sea necesario)
CMD ["python", "remotetypes/command_handlers.py"]
