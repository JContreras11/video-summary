#!/usr/bin/env python3
"""
Script de ejecución para la Video Summarization API
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import fastapi
        import uvicorn
        import openai
        import anthropic
        import google.generativeai
        import whisper
        import moviepy
        print("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("Ejecuta: pip install -r requirements.txt")
        return False

def check_env_file():
    """Verifica que el archivo .env exista"""
    if not os.path.exists('.env'):
        print("⚠️  Archivo .env no encontrado")
        print("Copiando env.example a .env...")
        try:
            import shutil
            shutil.copy('env.example', '.env')
            print("✅ Archivo .env creado. Edítalo con tus API keys.")
            return False
        except Exception as e:
            print(f"❌ Error creando .env: {e}")
            return False
    return True

def check_folders():
    """Verifica que las carpetas necesarias existan"""
    folders = ['videos', 'processed']
    for folder in folders:
        if not os.path.exists(folder):
            print(f"Creando carpeta: {folder}")
            os.makedirs(folder, exist_ok=True)
    print("✅ Carpetas verificadas")

def main():
    """Función principal"""
    print("🎥 Video Summarization API - Iniciando...\n")
    
    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)
    
    # Verificar archivo .env
    if not check_env_file():
        print("\n⚠️  IMPORTANTE: Edita el archivo .env con tus API keys antes de continuar")
        print("Ejemplo:")
        print("AI_PROVIDER=openai")
        print("OPENAI_API_KEY=tu_api_key_aqui")
        print("\n¿Deseas continuar de todas formas? (s/N): ", end="")
        response = input().lower()
        if response not in ['s', 'si', 'sí', 'y', 'yes']:
            sys.exit(0)
    
    # Verificar carpetas
    check_folders()
    
    print("\n🚀 Iniciando servidor...")
    print("📖 Documentación disponible en: http://localhost:8000/docs")
    print("🔍 Health check en: http://localhost:8000/health")
    print("⏹️  Presiona Ctrl+C para detener\n")
    
    try:
        # Importar y ejecutar la aplicación
        from main import app
        import uvicorn
        from config import Config
        
        uvicorn.run(
            app,
            host=Config.HOST,
            port=Config.PORT,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
