import os
import logging
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from audio_processor import AudioProcessor
from ai_agents import AIAgentFactory
from config import Config

logger = logging.getLogger(__name__)

class VideoProcessor:
    """Procesador principal de videos para generar resúmenes"""
    
    def __init__(self):
        self.audio_processor = AudioProcessor()
        self.ai_agent = AIAgentFactory.create_agent()
        self.temp_files = []
    
    def process_video(self, video_path: str) -> Dict[str, Any]:
        """Procesa un video completo: extrae audio, transcribe y genera resumen"""
        try:
            logger.info(f"Iniciando procesamiento de video: {video_path}")
            
            # Validar archivo
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video no encontrado: {video_path}")
            
            # Obtener información del video
            video_info = self.audio_processor.get_video_info(video_path)
            logger.info(f"Información del video: {video_info}")
            
            # Validar tamaño
            if video_info["size_mb"] > Config.MAX_VIDEO_SIZE_MB:
                raise ValueError(f"Video demasiado grande: {video_info['size_mb']:.2f}MB > {Config.MAX_VIDEO_SIZE_MB}MB")
            
            # Validar formato
            if video_info["format"].lower() not in [fmt.lower() for fmt in Config.SUPPORTED_FORMATS]:
                raise ValueError(f"Formato no soportado: {video_info['format']}")
            
            # Extraer audio
            audio_path = self.audio_processor.extract_audio_from_video(video_path)
            self.temp_files.append(audio_path)
            
            # Transcribir audio
            transcript = self._transcribe_audio(audio_path)
            
            # Generar resumen
            summary = self.ai_agent.generate_summary(transcript, video_info)
            
            # Crear resultado
            result = {
                "video_path": video_path,
                "video_info": video_info,
                "transcript": transcript,
                "summary": summary,
                "processed_at": datetime.now().isoformat(),
                "ai_provider": Config.AI_PROVIDER,
                "transcription_model": Config.TRANSCRIPTION_MODEL
            }
            
            # Guardar resultado
            output_file = self._save_result(result, video_path)
            
            logger.info(f"Procesamiento completado exitosamente: {output_file}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error procesando video {video_path}: {e}")
            raise
        finally:
            # Limpiar archivos temporales
            self._cleanup_temp_files()
    
    def _transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio usando el método configurado"""
        try:
            if Config.TRANSCRIPTION_MODEL == "whisper":
                return self.audio_processor.transcribe_with_whisper(audio_path)
            else:
                # Usar el agente de IA para transcripción
                return self.ai_agent.transcribe_audio(audio_path)
        except Exception as e:
            logger.error(f"Error en transcripción: {e}")
            raise
    
    def _save_result(self, result: Dict[str, Any], video_path: str) -> str:
        """Guarda el resultado en un archivo de texto"""
        try:
            # Crear nombre de archivo de salida
            video_name = Path(video_path).stem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{video_name}_resumen_{timestamp}.txt"
            output_path = os.path.join(Config.VIDEO_OUTPUT_FOLDER, output_filename)
            
            # Crear contenido del archivo
            content = self._format_summary_content(result)
            
            # Guardar archivo
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Resumen guardado en: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error guardando resultado: {e}")
            raise
    
    def _format_summary_content(self, result: Dict[str, Any]) -> str:
        """Formatea el contenido del resumen para el archivo de texto"""
        content = f"""
RESUMEN DE VIDEO
{'='*50}

INFORMACIÓN DEL VIDEO:
- Archivo: {result['video_info']['format'].upper()}
- Duración: {result['video_info']['duration']:.2f} segundos
- Tamaño: {result['video_info']['size_mb']:.2f} MB
- Resolución: {result['video_info']['size'][0]}x{result['video_info']['size'][1]}
- FPS: {result['video_info']['fps']}

CONFIGURACIÓN:
- Proveedor de IA: {result['ai_provider'].upper()}
- Modelo de transcripción: {result['transcription_model'].upper()}
- Procesado el: {result['processed_at']}

TRANSCRIPCIÓN COMPLETA:
{'-'*30}
{result['transcript']}

RESUMEN GENERADO:
{'-'*30}
{result['summary']}

{'='*50}
        """
        return content.strip()
    
    def _cleanup_temp_files(self):
        """Limpia archivos temporales"""
        if self.temp_files:
            self.audio_processor.cleanup_temp_files(self.temp_files)
            self.temp_files = []
    
    def process_folder(self, folder_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """Procesa todos los videos en una carpeta"""
        if not folder_path:
            folder_path = Config.VIDEO_INPUT_FOLDER
        
        results = []
        supported_formats = [fmt.lower() for fmt in Config.SUPPORTED_FORMATS]
        
        try:
            logger.info(f"Procesando carpeta: {folder_path}")
            
            # Obtener archivos de video
            video_files = []
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    file_ext = Path(file).suffix.lower()[1:]  # Sin el punto
                    if file_ext in supported_formats:
                        video_files.append(file_path)
            
            if not video_files:
                logger.info("No se encontraron archivos de video para procesar")
                return results
            
            logger.info(f"Encontrados {len(video_files)} videos para procesar")
            
            # Procesar cada video
            for video_path in video_files:
                try:
                    result = self.process_video(video_path)
                    results.append(result)
                    logger.info(f"Video procesado exitosamente: {video_path}")
                except Exception as e:
                    logger.error(f"Error procesando {video_path}: {e}")
                    # Continuar con el siguiente video
            
            logger.info(f"Procesamiento de carpeta completado. {len(results)} videos procesados exitosamente")
            return results
            
        except Exception as e:
            logger.error(f"Error procesando carpeta {folder_path}: {e}")
            raise
    
    def get_processing_status(self) -> Dict[str, Any]:
        """Obtiene el estado del procesamiento"""
        return {
            "ai_provider": Config.AI_PROVIDER,
            "transcription_model": Config.TRANSCRIPTION_MODEL,
            "input_folder": Config.VIDEO_INPUT_FOLDER,
            "output_folder": Config.VIDEO_OUTPUT_FOLDER,
            "supported_formats": Config.SUPPORTED_FORMATS,
            "max_video_size_mb": Config.MAX_VIDEO_SIZE_MB,
            "temp_files_count": len(self.temp_files)
        }
