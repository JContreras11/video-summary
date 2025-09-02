#!/usr/bin/env python3
"""
Cliente de ejemplo para la Video Summarization API
Demuestra cómo usar los diferentes endpoints
"""

import requests
import json
import time
import os
from typing import Dict, Any

class VideoSummarizationClient:
    """Cliente para interactuar con la Video Summarization API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica el estado del servidor"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en health check: {e}")
            return {"status": "error", "message": str(e)}
    
    def process_video(self, video_path: str, callback_url: str = None) -> Dict[str, Any]:
        """Procesa un video específico"""
        try:
            payload = {
                "video_path": video_path
            }
            if callback_url:
                payload["callback_url"] = callback_url
            
            response = self.session.post(
                f"{self.base_url}/process-video",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error procesando video: {e}")
            return {"status": "error", "message": str(e)}
    
    def process_folder(self, folder_path: str = None, callback_url: str = None) -> Dict[str, Any]:
        """Procesa todos los videos en una carpeta"""
        try:
            payload = {}
            if folder_path:
                payload["folder_path"] = folder_path
            if callback_url:
                payload["callback_url"] = callback_url
            
            response = self.session.post(
                f"{self.base_url}/process-folder",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error procesando carpeta: {e}")
            return {"status": "error", "message": str(e)}
    
    def webhook_process(self, video_path: str = None, folder_path: str = None, callback_url: str = None) -> Dict[str, Any]:
        """Usa el webhook para procesar videos"""
        try:
            data = {}
            if video_path:
                data["video_path"] = video_path
            if folder_path:
                data["folder_path"] = folder_path
            if callback_url:
                data["callback_url"] = callback_url
            
            response = self.session.post(
                f"{self.base_url}/webhook/process",
                data=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en webhook: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Obtiene el estado de una tarea"""
        try:
            response = self.session.get(f"{self.base_url}/task/{task_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo estado de tarea: {e}")
            return {"status": "error", "message": str(e)}
    
    def list_tasks(self) -> Dict[str, Any]:
        """Lista todas las tareas"""
        try:
            response = self.session.get(f"{self.base_url}/tasks")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error listando tareas: {e}")
            return {"status": "error", "message": str(e)}
    
    def list_files(self) -> Dict[str, Any]:
        """Lista los archivos de resumen generados"""
        try:
            response = self.session.get(f"{self.base_url}/files")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error listando archivos: {e}")
            return {"status": "error", "message": str(e)}
    
    def download_file(self, filename: str, output_path: str = None) -> bool:
        """Descarga un archivo de resumen"""
        try:
            response = self.session.get(f"{self.base_url}/files/{filename}")
            response.raise_for_status()
            
            if not output_path:
                output_path = filename
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Archivo descargado: {output_path}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error descargando archivo: {e}")
            return False
    
    def wait_for_task_completion(self, task_id: str, timeout: int = 300, check_interval: int = 5) -> Dict[str, Any]:
        """Espera a que una tarea se complete"""
        print(f"Esperando completación de tarea: {task_id}")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_task_status(task_id)
            
            if status.get("status") in ["completed", "error"]:
                print(f"Tarea {task_id} completada con estado: {status.get('status')}")
                return status
            
            print(f"Estado actual: {status.get('status')} - Esperando {check_interval} segundos...")
            time.sleep(check_interval)
        
        print(f"Timeout esperando tarea {task_id}")
        return {"status": "timeout", "message": "Tiempo de espera agotado"}

def main():
    """Función principal de demostración"""
    print("=== Cliente de ejemplo para Video Summarization API ===\n")
    
    # Crear cliente
    client = VideoSummarizationClient()
    
    # 1. Verificar estado del servidor
    print("1. Verificando estado del servidor...")
    health = client.health_check()
    print(f"Estado: {json.dumps(health, indent=2)}\n")
    
    if health.get("status") != "healthy":
        print("❌ Servidor no está disponible. Asegúrate de que esté ejecutándose.")
        return
    
    print("✅ Servidor funcionando correctamente\n")
    
    # 2. Listar tareas existentes
    print("2. Listando tareas existentes...")
    tasks = client.list_tasks()
    print(f"Tareas: {json.dumps(tasks, indent=2)}\n")
    
    # 3. Listar archivos existentes
    print("3. Listando archivos de resumen...")
    files = client.list_files()
    print(f"Archivos: {json.dumps(files, indent=2)}\n")
    
    # 4. Ejemplo de procesamiento de video (comentado para evitar errores)
    print("4. Ejemplo de procesamiento de video...")
    print("⚠️  Descomenta las siguientes líneas y ajusta la ruta del video:")
    
    # video_path = "/ruta/al/video.mp4"  # Ajusta esta ruta
    # if os.path.exists(video_path):
    #     result = client.process_video(video_path)
    #     print(f"Resultado: {json.dumps(result, indent=2)}")
    #     
    #     if result.get("task_id"):
    #         # Esperar completación
    #         final_status = client.wait_for_task_completion(result["task_id"])
    #         print(f"Estado final: {json.dumps(final_status, indent=2)}")
    # else:
    #     print(f"❌ Video no encontrado: {video_path}")
    
    print("\n5. Ejemplo de procesamiento de carpeta...")
    print("⚠️  Descomenta las siguientes líneas y ajusta la ruta de la carpeta:")
    
    # folder_path = "./videos"  # Ajusta esta ruta
    # if os.path.exists(folder_path):
    #     result = client.process_folder(folder_path)
    #     print(f"Resultado: {json.dumps(result, indent=2)}")
    #     
    #     if result.get("task_id"):
    #         # Esperar completación
    #         final_status = client.wait_for_task_completion(result["task_id"])
    #         print(f"Estado final: {json.dumps(final_status, indent=2)}")
    # else:
    #     print(f"❌ Carpeta no encontrada: {folder_path}")
    
    print("\n=== Ejemplos de uso completados ===")
    print("\nPara usar el cliente:")
    print("1. Asegúrate de que el servidor esté ejecutándose")
    print("2. Configura las rutas de videos en el código")
    print("3. Descomenta las líneas de ejemplo")
    print("4. Ejecuta: python example_client.py")

if __name__ == "__main__":
    main()
