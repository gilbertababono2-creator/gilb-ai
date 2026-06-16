from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
import uuid
from backend.video_downloader import download_video
from backend.video_processor import video_processor
from backend.config import TEMP_DIR, OUTPUT_DIR
from typing import List, Optional

router = APIRouter()

# In-memory task status storage
tasks = {}

class VideoURL(BaseModel):
    url: str

class ClipRequest(BaseModel):
    video_path: str
    start_time: float
    end_time: float

class AIClipRequest(BaseModel):
    video_path: str
    language: Optional[str] = "en"

@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    extension = file.filename.split(".")[-1]
    file_path = os.path.join(TEMP_DIR, f"{file_id}.{extension}")

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {"video_path": file_path, "filename": file.filename}

@router.post("/download")
async def download_from_url(request: VideoURL):
    try:
        file_path = await download_video(request.url)
        return {"video_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/transcribe")
async def transcribe_video(request: AIClipRequest):
    try:
        transcription = await video_processor.transcribe(request.video_path, request.language)
        return {"transcription": transcription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clip")
async def clip_video(request: ClipRequest):
    try:
        clip_path = await video_processor.clip_video(request.video_path, request.start_time, request.end_time)
        return {"clip_path": clip_path, "filename": os.path.basename(clip_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai-clip")
async def ai_clip_video(request: AIClipRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "processing", "result": None}

    async def process_task(tid, vpath, lang):
        try:
            clips = await video_processor.auto_ai_clip(vpath, lang)
            tasks[tid] = {"status": "completed", "result": clips}
        except Exception as e:
            tasks[tid] = {"status": "failed", "error": str(e)}

    background_tasks.add_task(process_task, task_id, request.video_path, request.language)
    return {"task_id": task_id}

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@router.get("/clips/{filename}")
async def get_clip_url(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Clip not found")
    return {"url": f"/outputs/{filename}"}
