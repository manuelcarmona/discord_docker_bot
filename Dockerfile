# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la app al contenedor
COPY . /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto si es necesario (no esencial en este caso)
EXPOSE 8000

# Comando por defecto para ejecutar la app
CMD ["python", "app.py"]
