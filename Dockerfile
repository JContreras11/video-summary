# Usa una imagen base de Python
FROM python:3.9-slim

# Instala ffmpeg y utilidades necesarias
RUN apt-get update && apt-get install -y ffmpeg ca-certificates && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt y el script de instalación
COPY requirements.txt install.py ./

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Instalar Nginx
RUN apt-get update && apt-get install -y nginx

# Copiar el archivo de configuración de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Exponer el puerto 80 para Nginx
EXPOSE 80

# Comando para iniciar Nginx y tu aplicación
CMD service nginx start && python3 main.py