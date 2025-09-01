# Video Summarization API

Sistema de resumen de videos usando IA que extrae audio, transcribe y genera resúmenes detallados en español. Soporta múltiples proveedores de IA y funciona como webhook con FastAPI.

## Características

- 🎥 **Extracción de audio** de videos en múltiples formatos
- 🗣️ **Transcripción automática** usando Whisper o servicios de IA
- 🤖 **Resúmenes inteligentes** con OpenAI, Anthropic Claude o Google Gemini
- 🌐 **API REST** con FastAPI para integración fácil
- 🔄 **Webhook support** para procesamiento asíncrono
- 📁 **Procesamiento por lotes** de carpetas completas
- 📊 **Tracking de tareas** con estado en tiempo real
- 🔧 **Configuración flexible** con variables de entorno

## Proveedores de IA Soportados

- **OpenAI** (GPT-4, Whisper) - Requiere API key de pago
- **Anthropic** (Claude) - Requiere API key de pago
- **Google AI** (Gemini) - **Versión gratuita disponible** ✅

## Instalación

### 1. Clonar y configurar entorno

```bash
cd video-summarization
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
python install.py  # Script de instalación automática
```

**Alternativa manual:**
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copia el archivo de ejemplo y configura tus API keys:

```bash
cp env.example .env
```

**Para Google AI (versión gratuita):**
```bash
python setup_google_ai.py
```

**O edita manualmente `.env` con tus configuraciones:**

```env
# Selecciona tu proveedor de IA
AI_PROVIDER=openai  # openai, anthropic, google

# OpenAI Configuration
OPENAI_API_KEY=tu_api_key_de_openai
OPENAI_MODEL=gpt-4

# Anthropic Configuration
ANTHROPIC_API_KEY=tu_api_key_de_anthropic
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Google AI Configuration (versión gratuita)
GOOGLE_API_KEY=tu_api_key_de_google
GOOGLE_MODEL=gemini-1.5-flash

# Configuración de transcripción
TRANSCRIPTION_MODEL=whisper  # whisper, openai, anthropic
WHISPER_MODEL=base  # tiny, base, small, medium, large

# Carpetas de videos
VIDEO_INPUT_FOLDER=./videos
VIDEO_OUTPUT_FOLDER=./processed

# Configuración del servidor
HOST=0.0.0.0
PORT=3300
```

### 3. Crear carpetas necesarias

```bash
mkdir videos processed
```

## Uso

### Iniciar el servidor

```bash
python run.py  # Script de ejecución con verificaciones
```

O directamente:
```bash
python main.py
```

El servidor estará disponible en `http://localhost:3300`

### Documentación automática

- **Swagger UI**: `http://localhost:3300/docs`
- **ReDoc**: `http://localhost:3300/redoc`

## Endpoints de la API

### 1. Procesar video específico

```bash
curl -X POST "http://localhost:3300/process-video" \
  -H "Content-Type: application/json" \
  -d '{
    "video_path": "/ruta/al/video.mp4",
    "callback_url": "https://tu-webhook.com/callback"
  }'
```

### 2. Procesar carpeta completa

```bash
curl -X POST "http://localhost:3300/process-folder" \
  -H "Content-Type: application/json" \
  -d '{
    "folder_path": "/ruta/a/carpeta",
    "callback_url": "https://tu-webhook.com/callback"
  }'
```

### 3. Webhook para procesamiento

```bash
curl -X POST "http://localhost:3300/webhook/process" \
  -F "video_path=/ruta/al/video.mp4" \
  -F "callback_url=https://tu-webhook.com/callback"
```

### 4. Verificar estado de tarea

```bash
curl "http://localhost:3300/task/{task_id}"
```

### 5. Listar archivos generados

```bash
curl "http://localhost:3300/files"
```

### 6. Descargar resumen

```bash
curl "http://localhost:3300/files/{filename}" --output resumen.txt
```

## Formato de respuesta

### Respuesta de procesamiento

```json
{
  "task_id": "video_20241201_143022_123456",
  "status": "processing",
  "message": "Procesamiento iniciado",
  "timestamp": "2024-12-01T14:30:22.123456"
}
```

### Estado de tarea completada

```json
{
  "task_id": "video_20241201_143022_123456",
  "status": "completed",
  "results": [
    {
      "video_path": "/ruta/al/video.mp4",
      "video_info": {
        "duration": 120.5,
        "fps": 30.0,
        "size": [1920, 1080],
        "format": "mp4",
        "size_mb": 45.2,
        "has_audio": true
      },
      "transcript": "Transcripción completa del audio...",
      "summary": "Resumen generado por IA...",
      "processed_at": "2024-12-01T14:32:15.123456",
      "ai_provider": "openai",
      "transcription_model": "whisper"
    }
  ],
  "errors": [],
  "completed_at": "2024-12-01T14:32:15.123456"
}
```

## Webhook Callback

Cuando se configura un `callback_url`, el sistema enviará una notificación POST con:

```json
{
  "task_id": "video_20241201_143022_123456",
  "status": "completed",
  "results": [...],
  "errors": [],
  "timestamp": "2024-12-01T14:32:15.123456"
}
```

## Archivo de salida

Los resúmenes se guardan en archivos `.txt` con el formato:

```
RESUMEN DE VIDEO
==================================================

INFORMACIÓN DEL VIDEO:
- Archivo: MP4
- Duración: 120.50 segundos
- Tamaño: 45.20 MB
- Resolución: 1920x1080
- FPS: 30.0

CONFIGURACIÓN:
- Proveedor de IA: OPENAI
- Modelo de transcripción: WHISPER
- Procesado el: 2024-12-01T14:32:15.123456

TRANSCRIPCIÓN COMPLETA:
------------------------------
[Transcripción completa del audio]

RESUMEN GENERADO:
------------------------------
[Resumen estructurado generado por IA]

==================================================
```

## Configuración avanzada

### Límites de procesamiento

```env
MAX_VIDEO_SIZE_MB=100
SUPPORTED_FORMATS=mp4,avi,mov,mkv,webm
```

### Modelos de Whisper

- `tiny`: Más rápido, menos preciso
- `base`: Balance velocidad/precisión
- `small`: Mejor precisión
- `medium`: Alta precisión
- `large`: Máxima precisión

## Solución de problemas

### Error: "Modelo Whisper no está cargado"

```bash
# Asegúrate de tener suficiente RAM (al menos 2GB para modelo base)
# El primer inicio puede tardar varios minutos descargando el modelo
```

### Error: "API key no válida"

```bash
# Verifica que tu API key esté correctamente configurada en .env
# Asegúrate de que el proveedor seleccionado coincida con la key
```

### Error: "Video demasiado grande"

```bash
# Aumenta MAX_VIDEO_SIZE_MB en .env o comprime el video
```

### Error: "Formato no soportado"

```bash
# Verifica que el formato esté en SUPPORTED_FORMATS
# Convierte el video a un formato soportado
```

### Error: "Pydub no disponible"

```bash
# En Python 3.13, pydub puede tener problemas de compatibilidad
# El sistema funcionará sin pydub, pero algunas funcionalidades estarán limitadas
# Para instalar pydub: pip install pydub
```

### Error: "No module named 'moviepy.editor'"

```bash
# En versiones recientes de moviepy, usa: from moviepy import VideoFileClip
# El código ya está actualizado para manejar esto
```

## Desarrollo

### Estructura del proyecto

```
video-summarization/
├── main.py              # Aplicación FastAPI
├── config.py            # Configuración
├── ai_agents.py         # Agentes de IA
├── audio_processor.py   # Procesamiento de audio
├── video_processor.py   # Procesamiento de videos
├── requirements.txt     # Dependencias
├── env.example          # Variables de entorno
├── videos/              # Carpeta de entrada
├── processed/           # Carpeta de salida
└── README.md           # Documentación
```

### Agregar nuevo proveedor de IA

1. Implementa la clase en `ai_agents.py`
2. Agrega la configuración en `config.py`
3. Actualiza `AIAgentFactory`

## Licencia

MIT License - ver archivo LICENSE para detalles.

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request
