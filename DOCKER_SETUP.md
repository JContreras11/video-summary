# 🐳 Configuración Docker para Video Summarization

## ✅ Estado Actual
La configuración Docker ha sido corregida y está funcionando correctamente.

## 🚀 Inicio Rápido

### 1. Configurar el entorno
```bash
# Ejecutar el script de configuración
python3 setup_docker.py
```

### 2. Configurar variables de entorno
Edita el archivo `.env` con tus API keys:
```bash
# Configuración de IA - Selecciona un proveedor
AI_PROVIDER=google  # openai, anthropic, google

# Google AI Configuration (recomendado)
GOOGLE_API_KEY=tu_google_api_key_aqui
GOOGLE_MODEL=gemini-pro

# OpenAI Configuration (alternativo)
OPENAI_API_KEY=tu_openai_api_key_aqui
OPENAI_MODEL=gpt-4

# Anthropic Configuration (alternativo)
ANTHROPIC_API_KEY=tu_anthropic_api_key_aqui
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

### 3. Construir y ejecutar
```bash
# Construir la imagen
docker-compose -f docker-compose.local.yml build

# Ejecutar el contenedor
docker-compose -f docker-compose.local.yml up -d

# Ver logs
docker-compose -f docker-compose.local.yml logs -f
```

### 4. Probar la API
```bash
# Verificar salud del sistema
curl http://localhost:8080/health

# Ver información de la API
curl http://localhost:8080/
```

## 📁 Estructura de Archivos

```
video-summarization/
├── Dockerfile                 # Imagen Docker corregida
├── docker-compose.local.yml   # Configuración para desarrollo local
├── docker-compose.yml         # Configuración para producción
├── requirements.txt           # Dependencias Python actualizadas
├── setup_docker.py           # Script de configuración automática
├── .env                      # Variables de entorno (crear desde env.example)
├── videos/                   # Carpeta para videos de entrada
└── processed/                # Carpeta para resúmenes generados
```

## 🔧 Correcciones Realizadas

### Dockerfile
- ✅ Actualizado a Python 3.11 (desde 3.9)
- ✅ Instalado FFmpeg para procesamiento de video
- ✅ Instalado curl para healthchecks
- ✅ Optimizado para cache de Docker
- ✅ Eliminado Nginx innecesario

### docker-compose.local.yml
- ✅ Configuración simplificada para desarrollo
- ✅ Volúmenes montados correctamente
- ✅ Variables de entorno configuradas
- ✅ Healthcheck funcional

### requirements.txt
- ✅ Dependencias actualizadas
- ✅ Agregadas dependencias faltantes (Pillow, imageio, etc.)
- ✅ Versiones compatibles

## 🌐 Endpoints de la API

- `GET /` - Información de la API
- `GET /health` - Estado del sistema
- `POST /process-video` - Procesar un video específico
- `POST /process-folder` - Procesar todos los videos en una carpeta
- `GET /task/{task_id}` - Estado de una tarea
- `GET /files` - Listar archivos de resumen
- `GET /files/{filename}` - Descargar un resumen

## 🎥 Uso de la API

### Procesar un video
```bash
curl -X POST "http://localhost:8080/process-video" \
  -H "Content-Type: application/json" \
  -d '{"video_path": "/app/videos/mi_video.mp4"}'
```

### Procesar carpeta completa
```bash
curl -X POST "http://localhost:8080/process-folder" \
  -H "Content-Type: application/json" \
  -d '{"folder_path": "/app/videos"}'
```

## 🛠️ Comandos Útiles

```bash
# Ver logs en tiempo real
docker-compose -f docker-compose.local.yml logs -f

# Reiniciar el contenedor
docker-compose -f docker-compose.local.yml restart

# Detener el contenedor
docker-compose -f docker-compose.local.yml down

# Reconstruir desde cero
docker-compose -f docker-compose.local.yml down
docker-compose -f docker-compose.local.yml build --no-cache
docker-compose -f docker-compose.local.yml up -d

# Acceder al contenedor
docker-compose -f docker-compose.local.yml exec video-summarization bash
```

## 🔍 Solución de Problemas

### El contenedor no inicia
```bash
# Ver logs detallados
docker-compose -f docker-compose.local.yml logs

# Verificar configuración
docker-compose -f docker-compose.local.yml config
```

### Error de API Key
- Verifica que el archivo `.env` existe y tiene las API keys correctas
- Asegúrate de que `AI_PROVIDER` coincide con la API key configurada

### Error de permisos
```bash
# Dar permisos a las carpetas
chmod 755 videos processed
```

## 📊 Monitoreo

La aplicación incluye:
- ✅ Healthcheck automático
- ✅ Logs estructurados
- ✅ Métricas de procesamiento
- ✅ Manejo de errores robusto

## 🎯 Próximos Pasos

1. Configura tus API keys en `.env`
2. Coloca videos en la carpeta `videos/`
3. Ejecuta el procesamiento via API
4. Descarga los resúmenes desde `processed/`

¡La aplicación está lista para usar! 🚀
