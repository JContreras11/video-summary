import os
import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import uvicorn

from config import Config
from video_processor import VideoProcessor

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Video Summarization API",
    description="API para generar resúmenes de videos usando IA",
    version="1.0.0"
)

# Modelos Pydantic
class ProcessingRequest(BaseModel):
    video_path: Optional[str] = None
    folder_path: Optional[str] = None
    callback_url: Optional[str] = None

class ProcessingResponse(BaseModel):
    task_id: str
    status: str
    message: str
    timestamp: str

class ProcessingResult(BaseModel):
    task_id: str
    status: str
    results: List[Dict[str, Any]]
    errors: List[str]
    completed_at: str

# Variables globales para tracking de tareas
processing_tasks = {}

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    try:
        # Validar configuración
        errors = Config.validate_config()
        if errors:
            logger.error(f"Errores de configuración: {errors}")
            raise Exception(f"Configuración inválida: {errors}")
        
        logger.info("Aplicación iniciada correctamente")
        logger.info(f"Proveedor de IA: {Config.AI_PROVIDER}")
        logger.info(f"Modelo de transcripción: {Config.TRANSCRIPTION_MODEL}")
        logger.info(f"Carpeta de entrada: {Config.VIDEO_INPUT_FOLDER}")
        logger.info(f"Carpeta de salida: {Config.VIDEO_OUTPUT_FOLDER}")
        
    except Exception as e:
        logger.error(f"Error en el inicio: {e}")
        raise

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Video Summarization API",
        "version": "1.0.0",
        "status": "running",
        "ai_provider": Config.AI_PROVIDER,
        "transcription_model": Config.TRANSCRIPTION_MODEL
    }

@app.get("/health")
async def health_check():
    """Verificación de salud del sistema"""
    try:
        processor = VideoProcessor()
        status = processor.get_processing_status()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "config": status
        }
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-video", response_model=ProcessingResponse)
async def process_video(
    background_tasks: BackgroundTasks,
    request: ProcessingRequest
):
    """Procesa un video específico"""
    try:
        if not request.video_path:
            raise HTTPException(status_code=400, detail="video_path es requerido")
        
        # Generar ID de tarea
        task_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Inicializar tarea
        processing_tasks[task_id] = {
            "status": "processing",
            "results": [],
            "errors": [],
            "started_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        # Ejecutar procesamiento en background
        background_tasks.add_task(
            process_video_task,
            task_id,
            request.video_path,
            request.callback_url
        )
        
        return ProcessingResponse(
            task_id=task_id,
            status="processing",
            message="Procesamiento iniciado",
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error iniciando procesamiento: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-folder", response_model=ProcessingResponse)
async def process_folder(
    background_tasks: BackgroundTasks,
    request: ProcessingRequest
):
    """Procesa todos los videos en una carpeta"""
    try:
        folder_path = request.folder_path or Config.VIDEO_INPUT_FOLDER
        
        # Generar ID de tarea
        task_id = f"folder_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Inicializar tarea
        processing_tasks[task_id] = {
            "status": "processing",
            "results": [],
            "errors": [],
            "started_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        # Ejecutar procesamiento en background
        background_tasks.add_task(
            process_folder_task,
            task_id,
            folder_path,
            request.callback_url
        )
        
        return ProcessingResponse(
            task_id=task_id,
            status="processing",
            message="Procesamiento de carpeta iniciado",
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error iniciando procesamiento de carpeta: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/task/{task_id}", response_model=ProcessingResult)
async def get_task_status(task_id: str):
    """Obtiene el estado de una tarea de procesamiento"""
    if task_id not in processing_tasks:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    task = processing_tasks[task_id]
    
    return ProcessingResult(
        task_id=task_id,
        status=task["status"],
        results=task["results"],
        errors=task["errors"],
        completed_at=task["completed_at"] or datetime.now().isoformat()
    )

@app.get("/tasks")
async def list_tasks():
    """Lista todas las tareas de procesamiento"""
    return {
        "tasks": processing_tasks,
        "total": len(processing_tasks)
    }

@app.post("/webhook/process")
async def webhook_process(
    background_tasks: BackgroundTasks,
    video_path: Optional[str] = Form(None),
    folder_path: Optional[str] = Form(None),
    callback_url: Optional[str] = Form(None)
):
    """Webhook para procesamiento de videos"""
    try:
        if video_path:
            # Procesar video específico
            task_id = f"webhook_video_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            processing_tasks[task_id] = {
                "status": "processing",
                "results": [],
                "errors": [],
                "started_at": datetime.now().isoformat(),
                "completed_at": None
            }
            
            background_tasks.add_task(
                process_video_task,
                task_id,
                video_path,
                callback_url
            )
            
        elif folder_path:
            # Procesar carpeta
            task_id = f"webhook_folder_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            processing_tasks[task_id] = {
                "status": "processing",
                "results": [],
                "errors": [],
                "started_at": datetime.now().isoformat(),
                "completed_at": None
            }
            
            background_tasks.add_task(
                process_folder_task,
                task_id,
                folder_path,
                callback_url
            )
        else:
            raise HTTPException(status_code=400, detail="video_path o folder_path es requerido")
        
        return {
            "task_id": task_id,
            "status": "processing",
            "message": "Procesamiento iniciado via webhook",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error en webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files")
async def list_output_files():
    """Lista los archivos de resumen generados"""
    try:
        files = []
        if os.path.exists(Config.VIDEO_OUTPUT_FOLDER):
            for file in os.listdir(Config.VIDEO_OUTPUT_FOLDER):
                if file.endswith('.txt'):
                    file_path = os.path.join(Config.VIDEO_OUTPUT_FOLDER, file)
                    file_stat = os.stat(file_path)
                    files.append({
                        "filename": file,
                        "size_bytes": file_stat.st_size,
                        "created_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                        "modified_at": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                    })
        
        return {
            "files": files,
            "total": len(files)
        }
        
    except Exception as e:
        logger.error(f"Error listando archivos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/{filename}")
async def download_file(filename: str):
    """Descarga un archivo de resumen"""
    try:
        file_path = os.path.join(Config.VIDEO_OUTPUT_FOLDER, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='text/plain'
        )
        
    except Exception as e:
        logger.error(f"Error descargando archivo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Funciones de background
async def process_video_task(task_id: str, video_path: str, callback_url: Optional[str] = None):
    """Tarea en background para procesar un video"""
    try:
        logger.info(f"Procesando video en background: {video_path}")
        
        processor = VideoProcessor()
        result = processor.process_video(video_path)
        
        # Actualizar tarea
        processing_tasks[task_id]["status"] = "completed"
        processing_tasks[task_id]["results"] = [result]
        processing_tasks[task_id]["completed_at"] = datetime.now().isoformat()
        
        logger.info(f"Video procesado exitosamente: {video_path}")
        
        # Enviar callback si está configurado
        if callback_url:
            await send_callback(callback_url, task_id, "completed", [result])
            
    except Exception as e:
        logger.error(f"Error procesando video {video_path}: {e}")
        
        # Actualizar tarea con error
        processing_tasks[task_id]["status"] = "error"
        processing_tasks[task_id]["errors"] = [str(e)]
        processing_tasks[task_id]["completed_at"] = datetime.now().isoformat()
        
        # Enviar callback de error si está configurado
        if callback_url:
            await send_callback(callback_url, task_id, "error", [], [str(e)])

async def process_folder_task(task_id: str, folder_path: str, callback_url: Optional[str] = None):
    """Tarea en background para procesar una carpeta"""
    try:
        logger.info(f"Procesando carpeta en background: {folder_path}")
        
        processor = VideoProcessor()
        results = processor.process_folder(folder_path)
        
        # Actualizar tarea
        processing_tasks[task_id]["status"] = "completed"
        processing_tasks[task_id]["results"] = results
        processing_tasks[task_id]["completed_at"] = datetime.now().isoformat()
        
        logger.info(f"Carpeta procesada exitosamente: {len(results)} videos")
        
        # Enviar callback si está configurado
        if callback_url:
            await send_callback(callback_url, task_id, "completed", results)
            
    except Exception as e:
        logger.error(f"Error procesando carpeta {folder_path}: {e}")
        
        # Actualizar tarea con error
        processing_tasks[task_id]["status"] = "error"
        processing_tasks[task_id]["errors"] = [str(e)]
        processing_tasks[task_id]["completed_at"] = datetime.now().isoformat()
        
        # Enviar callback de error si está configurado
        if callback_url:
            await send_callback(callback_url, task_id, "error", [], [str(e)])

async def send_callback(url: str, task_id: str, status: str, results: List[Dict], errors: List[str] = None):
    """Envía callback a URL especificada"""
    try:
        import aiohttp
        
        payload = {
            "task_id": task_id,
            "status": status,
            "results": results,
            "errors": errors or [],
            "timestamp": datetime.now().isoformat()
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                logger.info(f"Callback enviado a {url}: {response.status}")
                
    except Exception as e:
        logger.error(f"Error enviando callback a {url}: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True,
        log_level="info"
    )
