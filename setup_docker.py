#!/usr/bin/env python3
"""
Script para configurar el entorno Docker para video-summarization
"""

import os
import shutil
from pathlib import Path

def setup_docker_environment():
    """Configura el entorno Docker"""
    print("🐳 Configurando entorno Docker para video-summarization...")
    
    # Verificar si existe .env
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("📋 Creando archivo .env desde env.example...")
            shutil.copy(env_example, env_file)
            print("✅ Archivo .env creado. Por favor, edita las API keys necesarias.")
        else:
            print("❌ No se encontró env.example")
            return False
    else:
        print("✅ Archivo .env ya existe")
    
    # Crear directorios necesarios
    directories = ["videos", "processed"]
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"📁 Creando directorio: {directory}")
            dir_path.mkdir(exist_ok=True)
        else:
            print(f"✅ Directorio {directory} ya existe")
    
    # Verificar Docker
    print("\n🔍 Verificando Docker...")
    if shutil.which("docker"):
        print("✅ Docker está instalado")
    else:
        print("❌ Docker no está instalado. Por favor, instala Docker Desktop.")
        return False
    
    if shutil.which("docker-compose"):
        print("✅ Docker Compose está instalado")
    else:
        print("❌ Docker Compose no está instalado. Por favor, instala Docker Compose.")
        return False
    
    print("\n🎉 Configuración completada!")
    print("\n📝 Próximos pasos:")
    print("1. Edita el archivo .env con tus API keys")
    print("2. Ejecuta: docker-compose -f docker-compose.local.yml up --build")
    print("3. La aplicación estará disponible en http://localhost:8080")
    
    return True

if __name__ == "__main__":
    setup_docker_environment()
