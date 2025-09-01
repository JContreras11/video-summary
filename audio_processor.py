import os
import whisper
import logging
from moviepy import VideoFileClip
from typing import Dict, Any, Optional
import tempfile

# Importar pydub de manera condicional para evitar problemas con Python 3.13
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("⚠️ Pydub no disponible - algunas funcionalidades estarán limitadas")

logger = logging.getLogger(__name__)

class AudioProcessor:
    """Procesador de audio para extraer y transcribir audio de videos"""
    
    def __init__(self):
        self.whisper_model = None
        self._load_whisper_model()
    
    def _load_whisper_model(self):
        """Carga el modelo de Whisper"""
        try:
            from config import Config
            model_name = Config.WHISPER_MODEL
            logger.info(f"Cargando modelo Whisper: {model_name}")
            self.whisper_model = whisper.load_model(model_name)
            logger.info("Modelo Whisper cargado exitosamente")
        except Exception as e:
            logger.error(f"Error cargando modelo Whisper: {e}")
            raise
    
    def extract_audio_from_video(self, video_path: str, output_path: Optional[str] = None) -> str:
        """Extrae audio de un video y retorna la ruta del archivo de audio"""
        try:
            if not output_path:
                # Crear archivo temporal
                temp_dir = tempfile.gettempdir()
                video_name = os.path.splitext(os.path.basename(video_path))[0]
                output_path = os.path.join(temp_dir, f"{video_name}_audio.wav")
            
            logger.info(f"Extrayendo audio de: {video_path}")
            
            # Cargar video
            video = VideoFileClip(video_path)
            
            # Extraer audio
            audio = video.audio
            
            if audio is None:
                raise ValueError("El video no contiene audio")
            
            # Guardar audio
            audio.write_audiofile(output_path, logger=None)
            
            # Cerrar archivos
            video.close()
            audio.close()
            
            logger.info(f"Audio extraído exitosamente a: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error extrayendo audio: {e}")
            raise
    
    def transcribe_with_whisper(self, audio_path: str) -> str:
        """Transcribe audio usando Whisper local"""
        try:
            if not self.whisper_model:
                raise ValueError("Modelo Whisper no está cargado")
            
            logger.info(f"Transcribiendo audio: {audio_path}")
            
            # Transcribir
            result = self.whisper_model.transcribe(audio_path)
            transcript = result["text"]
            
            logger.info("Transcripción completada exitosamente")
            return transcript
            
        except Exception as e:
            logger.error(f"Error transcribiendo con Whisper: {e}")
            raise
    
    def get_video_info(self, video_path: str) -> Dict[str, Any]:
        """Obtiene información del video"""
        try:
            video = VideoFileClip(video_path)
            
            info = {
                "duration": video.duration,
                "fps": video.fps,
                "size": video.size,
                "format": os.path.splitext(video_path)[1][1:],
                "size_mb": os.path.getsize(video_path) / (1024 * 1024),
                "has_audio": video.audio is not None
            }
            
            video.close()
            return info
            
        except Exception as e:
            logger.error(f"Error obteniendo información del video: {e}")
            raise
    
    def cleanup_temp_files(self, file_paths: list):
        """Limpia archivos temporales"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Archivo temporal eliminado: {file_path}")
            except Exception as e:
                logger.warning(f"No se pudo eliminar archivo temporal {file_path}: {e}")
    
    def convert_audio_format(self, audio_path: str, target_format: str = "wav") -> str:
        """Convierte audio a formato específico"""
        if not PYDUB_AVAILABLE:
            raise ImportError("Pydub no está disponible para conversión de audio")
            
        try:
            # Cargar audio
            audio = AudioSegment.from_file(audio_path)
            
            # Crear archivo de salida
            output_path = os.path.splitext(audio_path)[0] + f".{target_format}"
            
            # Exportar
            audio.export(output_path, format=target_format)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error convirtiendo formato de audio: {e}")
            raise
