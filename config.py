import os
from typing import List
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración centralizada del sistema"""
    
    # Configuración del servidor
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 3300))
    
    # Carpetas de videos
    VIDEO_INPUT_FOLDER = os.getenv("VIDEO_INPUT_FOLDER", "./videos")
    VIDEO_OUTPUT_FOLDER = os.getenv("VIDEO_OUTPUT_FOLDER", "./processed")
    
    # Proveedor de IA
    AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()
    
    # Configuración OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Configuración Anthropic
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
    
    # Configuración Google AI
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-pro")
    
    # Configuración de transcripción
    TRANSCRIPTION_MODEL = os.getenv("TRANSCRIPTION_MODEL", "whisper").lower()
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
    
    # Configuración de procesamiento
    MAX_VIDEO_SIZE_MB = int(os.getenv("MAX_VIDEO_SIZE_MB", 1000))
    SUPPORTED_FORMATS = os.getenv("SUPPORTED_FORMATS", "mp4,avi,mov,mkv,webm").split(",")
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """Valida la configuración y retorna errores si los hay"""
        errors = []
        
        # Crear carpetas si no existen
        os.makedirs(cls.VIDEO_INPUT_FOLDER, exist_ok=True)
        os.makedirs(cls.VIDEO_OUTPUT_FOLDER, exist_ok=True)
        
        # Validar proveedor de IA
        if cls.AI_PROVIDER not in ["openai", "anthropic", "google"]:
            errors.append(f"Proveedor de IA no válido: {cls.AI_PROVIDER}")
        
        # Validar API keys según el proveedor
        if cls.AI_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY es requerida para el proveedor OpenAI")
        elif cls.AI_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            errors.append("ANTHROPIC_API_KEY es requerida para el proveedor Anthropic")
        elif cls.AI_PROVIDER == "google" and not cls.GOOGLE_API_KEY:
            errors.append("GOOGLE_API_KEY es requerida para el proveedor Google")
        
        return errors
