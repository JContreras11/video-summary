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

# Expone el puerto en el que la aplicación correrá (coincide con Config.PORT)
EXPOSE 80

# Comando por defecto: uvicorn (producción sin reload)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "info"]