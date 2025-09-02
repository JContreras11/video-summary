# Usa una imagen base de Python
FROM python:3.9-slim

# Instalar Nginx
RUN apt-get update && apt-get install -y nginx

# Copiar el archivo de configuración de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar el código de la aplicación
COPY . /app
WORKDIR /app

# Exponer el puerto 80 para Nginx
EXPOSE 80

# Comando para iniciar Nginx y tu aplicación
CMD service nginx start && uvicorn main:app --host 0.0.0.0 --port 3300