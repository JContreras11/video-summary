#!/usr/bin/env python3
"""
Script para configurar Google AI API
"""

import os
import sys
from pathlib import Path

def setup_google_ai():
    """Configura Google AI API"""
    print("🔧 Configurando Google AI API...\n")
    
    # Verificar si existe el archivo .env
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Archivo .env no encontrado")
        print("Ejecuta primero: cp env.example .env")
        return False
    
    # Leer configuración actual
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Verificar si ya está configurado
    if "your_google_api_key_here" not in content:
        print("✅ Google AI ya está configurado")
        return True
    
    print("📝 Para usar Google AI (versión gratuita), necesitas:")
    print("1. Ir a: https://makersuite.google.com/app/apikey")
    print("2. Crear una nueva API key")
    print("3. Copiar la key aquí\n")
    
    # Solicitar API key
    api_key = input("🔑 Ingresa tu Google API Key: ").strip()
    
    if not api_key:
        print("❌ No se ingresó API key")
        return False
    
    if len(api_key) < 20:
        print("❌ API key parece ser muy corta")
        return False
    
    # Actualizar archivo .env
    try:
        new_content = content.replace("your_google_api_key_here", api_key)
        
        with open(env_file, 'w') as f:
            f.write(new_content)
        
        print("✅ API key configurada correctamente")
        
        # Verificar configuración
        print("\n🔍 Verificando configuración...")
        os.environ["GOOGLE_API_KEY"] = api_key
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            # Probar con un modelo simple
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content("Hola, ¿funcionas?")
            
            print("✅ Conexión con Google AI exitosa")
            print(f"📝 Respuesta de prueba: {response.text}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error conectando con Google AI: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error guardando API key: {e}")
        return False

def test_configuration():
    """Prueba la configuración"""
    print("\n🧪 Probando configuración...")
    
    try:
        from config import Config
        from ai_agents import AIAgentFactory
        
        print(f"✅ Proveedor de IA: {Config.AI_PROVIDER}")
        print(f"✅ Modelo: {Config.GOOGLE_MODEL}")
        
        # Crear agente
        agent = AIAgentFactory.create_agent()
        print(f"✅ Agente creado: {type(agent).__name__}")
        
        # Probar generación de contenido
        test_text = "Este es un texto de prueba para verificar que Google AI funciona correctamente."
        summary = agent.generate_summary(test_text, {"duration": 60, "format": "mp4", "size_mb": 10})
        
        print("✅ Generación de resumen exitosa")
        print(f"📝 Resumen de prueba: {summary[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        return False

def main():
    """Función principal"""
    print("🎥 Configuración de Google AI para Video Summarization\n")
    print("=" * 60)
    
    # Configurar Google AI
    if not setup_google_ai():
        print("\n❌ Configuración falló")
        sys.exit(1)
    
    # Probar configuración
    if not test_configuration():
        print("\n❌ Prueba de configuración falló")
        sys.exit(1)
    
    print("\n🎉 ¡Configuración completada exitosamente!")
    print("\n📝 Próximos pasos:")
    print("1. Ejecuta: python run.py")
    print("2. Procesa tu video: curl -X POST 'http://localhost:3300/process-video' -H 'Content-Type: application/json' -d '{\"video_path\": \"./videos/minuta_compressed.mp4\"}'")
    print("3. Accede a: http://localhost:3300/docs")

if __name__ == "__main__":
    main()
