# Usar una imagen base de Python
FROM python:slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la app al contenedor
COPY . /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt \
    && groupadd -r bot \
    && useradd -r -g bot bot
# Exponer el puerto si es necesario (no esencial en este caso)
EXPOSE 8000

# Cambiar el propietario de los archivos al nuevo usuario
RUN chown -R bot:bot /app

# Establecer el usuario no root
USER bot

# Comando por defecto para ejecutar la app
CMD ["python", "app.py"]
