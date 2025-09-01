#!/usr/bin/env python3
"""
Script de instalación para Video Summarization API
Maneja las dependencias de manera robusta
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Salida de error: {e.stderr}")
        return False

def install_basic_dependencies():
    """Instala dependencias básicas"""
    basic_deps = [
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0", 
        "python-multipart>=0.0.6",
        "pydantic>=2.6.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "aiofiles>=23.2.1",
        "aiohttp>=3.9.0"
    ]
    
    for dep in basic_deps:
        if not run_command(f"pip install {dep}", f"Instalando {dep}"):
            return False
    return True

def install_ai_dependencies():
    """Instala dependencias de IA"""
    ai_deps = [
        "openai>=1.3.7",
        "anthropic>=0.7.7", 
        "google-generativeai>=0.3.2"
    ]
    
    for dep in ai_deps:
        if not run_command(f"pip install {dep}", f"Instalando {dep}"):
            return False
    return True

def install_audio_dependencies():
    """Instala dependencias de audio"""
    audio_deps = [
        "moviepy>=1.0.3",
        "pydub>=0.25.1"
    ]
    
    for dep in audio_deps:
        if not run_command(f"pip install {dep}", f"Instalando {dep}"):
            return False
    return True

def install_torch():
    """Instala PyTorch según el sistema"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("🍎 Detectado macOS, instalando PyTorch...")
        return run_command("pip install torch torchvision torchaudio", "Instalando PyTorch para macOS")
    elif system == "Linux":
        print("🐧 Detectado Linux, instalando PyTorch...")
        return run_command("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu", "Instalando PyTorch para Linux")
    elif system == "Windows":
        print("🪟 Detectado Windows, instalando PyTorch...")
        return run_command("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu", "Instalando PyTorch para Windows")
    else:
        print(f"⚠️ Sistema no reconocido: {system}, intentando instalación genérica...")
        return run_command("pip install torch", "Instalando PyTorch genérico")

def install_whisper():
    """Instala Whisper"""
    return run_command("pip install openai-whisper", "Instalando OpenAI Whisper")

def install_numpy():
    """Instala NumPy"""
    return run_command("pip install numpy>=1.21.0", "Instalando NumPy")

def check_installation():
    """Verifica que todo esté instalado correctamente"""
    print("\n🔍 Verificando instalación...")
    
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
        print("✅ Todas las dependencias están instaladas correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False

def main():
    """Función principal de instalación"""
    print("🎥 Instalando Video Summarization API...\n")
    
    # Instalar dependencias en orden
    steps = [
        ("Dependencias básicas", install_basic_dependencies),
        ("Dependencias de IA", install_ai_dependencies),
        ("Dependencias de audio", install_audio_dependencies),
        ("PyTorch", install_torch),
        ("Whisper", install_whisper),
        ("NumPy", install_numpy)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📦 {step_name}")
        print("=" * 50)
        if not step_func():
            print(f"\n❌ Error instalando {step_name}")
            print("Intenta instalar manualmente o revisa los errores")
            sys.exit(1)
    
    # Verificar instalación
    if check_installation():
        print("\n🎉 ¡Instalación completada exitosamente!")
        print("\n📝 Próximos pasos:")
        print("1. Copia env.example a .env: cp env.example .env")
        print("2. Edita .env con tus API keys")
        print("3. Ejecuta: python run.py")
    else:
        print("\n❌ Error en la verificación de instalación")
        sys.exit(1)

if __name__ == "__main__":
    main()
