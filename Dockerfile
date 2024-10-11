# Usar una imagen base de Python
FROM python:3.11-alpine

# Instalar dependencias del sistema
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la app al contenedor
COPY . /app

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto para ejecutar la app
CMD ["python", "app.py"]
