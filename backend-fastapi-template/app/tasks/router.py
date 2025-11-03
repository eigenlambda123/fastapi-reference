from fastapi import APIRouter, BackgroundTasks, UploadFile, File
from pathlib import Path
from app.tasks.utils import simulate_long_task, save_uploaded_file

router = APIRouter(prefix="/tasks", tags=["tasks"])

UPLOAD_DIR = Path("uploaded_files")

@router.post("/process")
def run_background_task(background_tasks: BackgroundTasks, seconds: int = 5):
    """Trigger a background task that runs for a few seconds."""
    background_tasks.add_task(simulate_long_task, seconds)
    return {"message": f"Background task started for {seconds} seconds"}

@router.post("/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Upload a file asynchronously using background task."""
    UPLOAD_DIR.mkdir(exist_ok=True)
    file_path = UPLOAD_DIR / file.filename
    content = await file.read()
    background_tasks.add_task(save_uploaded_file, file_path, content)
    return {"message": f"File {file.filename} is being processed in background"}
