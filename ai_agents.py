import openai
import anthropic
import google.generativeai as genai
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import logging
from config import Config

logger = logging.getLogger(__name__)

class AIAgent(ABC):
    """Clase abstracta para agentes de IA"""
    
    @abstractmethod
    def generate_summary(self, transcript: str, video_info: Dict[str, Any]) -> str:
        """Genera un resumen del transcript"""
        pass
    
    @abstractmethod
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio a texto"""
        pass

class OpenAIAgent(AIAgent):
    """Agente de OpenAI"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
    
    def generate_summary(self, transcript: str, video_info: Dict[str, Any]) -> str:
        """Genera resumen usando OpenAI"""
        try:
            prompt = f"""
            Analiza la siguiente transcripción de un video y crea un resumen detallado en español.
            
            Información del video:
            - Duración: {video_info.get('duration', 'N/A')}
            - Formato: {video_info.get('format', 'N/A')}
            - Tamaño: {video_info.get('size_mb', 'N/A')} MB
            
            Transcripción:
            {transcript}
            
            Por favor, crea un resumen estructurado que incluya:
            1. Tema principal del video
            2. Puntos clave discutidos
            3. Conclusiones importantes
            4. Palabras clave relevantes
            
            Resumen:
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en análisis de contenido multimedia. Crea resúmenes claros y estructurados."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generando resumen con OpenAI: {e}")
            raise
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio usando OpenAI Whisper"""
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript
        except Exception as e:
            logger.error(f"Error transcribiendo con OpenAI: {e}")
            raise

class AnthropicAgent(AIAgent):
    """Agente de Anthropic"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = Config.ANTHROPIC_MODEL
    
    def generate_summary(self, transcript: str, video_info: Dict[str, Any]) -> str:
        """Genera resumen usando Anthropic Claude"""
        try:
            prompt = f"""
            Analiza la siguiente transcripción de un video y crea un resumen detallado en español.
            
            Información del video:
            - Duración: {video_info.get('duration', 'N/A')}
            - Formato: {video_info.get('format', 'N/A')}
            - Tamaño: {video_info.get('size_mb', 'N/A')} MB
            
            Transcripción:
            {transcript}
            
            Por favor, crea un resumen estructurado que incluya:
            1. Tema principal del video
            2. Puntos clave discutidos
            3. Conclusiones importantes
            4. Palabras clave relevantes
            
            Resumen:
            """
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"Error generando resumen con Anthropic: {e}")
            raise
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio usando Anthropic (requiere archivo de audio)"""
        try:
            with open(audio_file_path, "rb") as audio_file:
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=4000,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Transcribe el audio de este archivo de manera precisa y detallada."
                                },
                                {
                                    "type": "audio",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "audio/wav",
                                        "data": audio_file.read()
                                    }
                                }
                            ]
                        }
                    ]
                )
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Error transcribiendo con Anthropic: {e}")
            raise

class GoogleAIAgent(AIAgent):
    """Agente de Google AI"""
    
    def __init__(self):
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY es requerida para usar Google AI")
        
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        # Usar el modelo configurado o fallback a gemini-1.5-flash
        try:
            self.model = genai.GenerativeModel(Config.GOOGLE_MODEL)
            # Verificar que el modelo esté disponible
            self.model.generate_content("test")
        except Exception as e:
            logger.warning(f"Modelo {Config.GOOGLE_MODEL} no disponible, usando gemini-1.5-flash")
            self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def generate_summary(self, transcript: str, video_info: Dict[str, Any]) -> str:
        """Genera resumen usando Google Gemini"""
        try:
            # Si el transcript es muy largo, dividirlo en chunks
            max_chunk_length = 30000  # Caracteres por chunk
            transcript_chunks = []
            
            if len(transcript) > max_chunk_length:
                # Dividir en chunks de tamaño razonable
                for i in range(0, len(transcript), max_chunk_length):
                    chunk = transcript[i:i + max_chunk_length]
                    transcript_chunks.append(chunk)
                logger.info(f"Transcript dividido en {len(transcript_chunks)} chunks")
            else:
                transcript_chunks = [transcript]
            
            summaries = []
            
            for i, chunk in enumerate(transcript_chunks):
                chunk_prompt = f"""
                Analiza la siguiente parte {i+1}/{len(transcript_chunks)} de la transcripción de un video y crea un resumen en español.
                
                Información del video:
                - Duración: {video_info.get('duration', 'N/A')} segundos
                - Formato: {video_info.get('format', 'N/A')}
                - Tamaño: {video_info.get('size_mb', 'N/A')} MB
                
                Transcripción (parte {i+1}/{len(transcript_chunks)}):
                {chunk}
                
                Crea un resumen estructurado que incluya:
                1. Tema principal de esta parte
                2. Puntos clave discutidos
                3. Información importante
                
                Resumen:
                """
                
                response = self.model.generate_content(chunk_prompt)
                summaries.append(response.text.strip())
            
            # Si hay múltiples chunks, crear un resumen final
            if len(summaries) > 1:
                final_prompt = f"""
                Combina los siguientes resúmenes de partes de un video en un resumen final coherente en español:
                
                {chr(10).join([f"Parte {i+1}: {summary}" for i, summary in enumerate(summaries)])}
                
                Crea un resumen final estructurado que incluya:
                1. Tema principal del video completo
                2. Puntos clave discutidos
                3. Conclusiones importantes
                4. Palabras clave relevantes
                
                Resumen final:
                """
                
                final_response = self.model.generate_content(final_prompt)
                return final_response.text.strip()
            else:
                return summaries[0]
            
        except Exception as e:
            logger.error(f"Error generando resumen con Google AI: {e}")
            raise
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Google AI no tiene transcripción directa, usar Whisper local"""
        # Para Google AI, usaremos Whisper local como fallback
        from audio_processor import AudioProcessor
        processor = AudioProcessor()
        return processor.transcribe_with_whisper(audio_file_path)

class AIAgentFactory:
    """Factory para crear agentes de IA según la configuración"""
    
    @staticmethod
    def create_agent() -> AIAgent:
        """Crea y retorna el agente de IA configurado"""
        provider = Config.AI_PROVIDER
        
        if provider == "openai":
            return OpenAIAgent()
        elif provider == "anthropic":
            return AnthropicAgent()
        elif provider == "google":
            return GoogleAIAgent()
        else:
            raise ValueError(f"Proveedor de IA no soportado: {provider}")
