# Usar una imagen base de Python
FROM python:alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la app al contenedor
COPY . /app

USER root

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt \
    && addgroup -S bot \
    && adduser -S -G bot bot

# Exponer el puerto si es necesario (no esencial en este caso)
EXPOSE 8000

# Cambiar el propietario de los archivos al nuevo usuario
RUN chown -R bot:bot /app

# Establecer el usuario no root
USER bot

# Comando por defecto para ejecutar la app
CMD ["python", "app.py"]
