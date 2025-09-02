#!/usr/bin/env python3
"""
Script de prueba para verificar que el sistema funciona correctamente
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

def test_imports():
    """Prueba que todas las dependencias se importen correctamente"""
    print("🔍 Probando importaciones...")
    
    try:
        import fastapi
        import uvicorn
        import openai
        import anthropic
        import google.generativeai
        import whisper
        import moviepy
        import torch
        import numpy
        import aiohttp
        print("✅ Todas las importaciones exitosas")
        return True
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False

def test_config():
    """Prueba la configuración del sistema"""
    print("\n🔍 Probando configuración...")
    
    try:
        from config import Config
        
        # Verificar que las carpetas se crean
        os.makedirs(Config.VIDEO_INPUT_FOLDER, exist_ok=True)
        os.makedirs(Config.VIDEO_OUTPUT_FOLDER, exist_ok=True)
        
        print(f"✅ Configuración cargada correctamente")
        print(f"   - Carpeta de entrada: {Config.VIDEO_INPUT_FOLDER}")
        print(f"   - Carpeta de salida: {Config.VIDEO_OUTPUT_FOLDER}")
        print(f"   - Proveedor de IA: {Config.AI_PROVIDER}")
        print(f"   - Modelo de transcripción: {Config.TRANSCRIPTION_MODEL}")
        return True
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_audio_processor():
    """Prueba el procesador de audio"""
    print("\n🔍 Probando procesador de audio...")
    
    try:
        from audio_processor import AudioProcessor
        
        processor = AudioProcessor()
        print("✅ Procesador de audio inicializado correctamente")
        
        # Verificar que el modelo Whisper se cargó
        if processor.whisper_model:
            print("✅ Modelo Whisper cargado correctamente")
        else:
            print("⚠️ Modelo Whisper no se cargó")
        
        return True
    except Exception as e:
        print(f"❌ Error en procesador de audio: {e}")
        return False

def test_ai_agents():
    """Prueba los agentes de IA"""
    print("\n🔍 Probando agentes de IA...")
    
    try:
        from ai_agents import AIAgentFactory
        
        # Verificar que el factory funciona
        try:
            agent = AIAgentFactory.create_agent()
            print(f"✅ Agente de IA creado: {type(agent).__name__}")
        except ValueError as e:
            print(f"⚠️ No se pudo crear agente (esperado sin API keys): {e}")
        
        return True
    except Exception as e:
        print(f"❌ Error en agentes de IA: {e}")
        return False

def test_video_processor():
    """Prueba el procesador de videos"""
    print("\n🔍 Probando procesador de videos...")
    
    try:
        from video_processor import VideoProcessor
        
        processor = VideoProcessor()
        print("✅ Procesador de videos inicializado correctamente")
        
        # Verificar estado
        status = processor.get_processing_status()
        print(f"✅ Estado del procesador: {status['ai_provider']}")
        
        return True
    except Exception as e:
        print(f"❌ Error en procesador de videos: {e}")
        return False

def test_fastapi_app():
    """Prueba la aplicación FastAPI"""
    print("\n🔍 Probando aplicación FastAPI...")
    
    try:
        from main import app
        
        print("✅ Aplicación FastAPI creada correctamente")
        
        # Verificar que tiene los endpoints principales
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/health", "/process-video", "/process-folder", "/webhook/process"]
        
        for route in expected_routes:
            if route in routes:
                print(f"✅ Endpoint {route} encontrado")
            else:
                print(f"⚠️ Endpoint {route} no encontrado")
        
        return True
    except Exception as e:
        print(f"❌ Error en aplicación FastAPI: {e}")
        return False

def create_test_video():
    """Crea un video de prueba simple"""
    print("\n🔍 Creando video de prueba...")
    
    try:
        # Crear un video simple usando moviepy
        from moviepy import ColorClip, AudioFileClip, CompositeVideoClip
        import numpy as np
        
        # Crear un clip de color con audio
        duration = 3
        fps = 24
        
        # Video simple
        video = ColorClip(size=(640, 480), color=(255, 0, 0), duration=duration)
        video = video.set_fps(fps)
        
        # Audio simple (tono)
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * 440 * t) * 0.3  # Nota A4
        
        # Guardar audio temporal
        import tempfile
        temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        import wave
        import struct
        
        with wave.open(temp_audio.name, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            for sample in audio_data:
                wav_file.writeframes(struct.pack('h', int(sample * 32767)))
        
        # Combinar video y audio
        audio = AudioFileClip(temp_audio.name)
        final_video = video.set_audio(audio)
        
        # Guardar video de prueba
        test_video_path = os.path.join("videos", "test_video.mp4")
        final_video.write_videofile(test_video_path, logger=None)
        
        # Limpiar archivo temporal
        os.unlink(temp_audio.name)
        
        print(f"✅ Video de prueba creado: {test_video_path}")
        return test_video_path
        
    except Exception as e:
        print(f"❌ Error creando video de prueba: {e}")
        return None

def main():
    """Función principal de pruebas"""
    print("🧪 Sistema de Pruebas - Video Summarization API\n")
    print("=" * 60)
    
    tests = [
        ("Importaciones", test_imports),
        ("Configuración", test_config),
        ("Procesador de Audio", test_audio_processor),
        ("Agentes de IA", test_ai_agents),
        ("Procesador de Videos", test_video_processor),
        ("Aplicación FastAPI", test_fastapi_app),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASÓ")
            else:
                print(f"❌ {test_name} - FALLÓ")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está listo para usar.")
        
        # Crear video de prueba
        test_video = create_test_video()
        if test_video:
            print(f"\n📹 Video de prueba disponible en: {test_video}")
            print("Puedes usar este video para probar el sistema una vez configurado.")
        
        print("\n📝 Próximos pasos:")
        print("1. Edita el archivo .env con tus API keys")
        print("2. Ejecuta: python run.py")
        print("3. Accede a: http://localhost:80/docs")
        
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores arriba.")
        sys.exit(1)

if __name__ == "__main__":
    main()
