from fastapi import APIRouter, UploadFile, File, HTTPException
from .utils import transcribe_audio

router = APIRouter(prefix="/stt", tags=["AI"])

@router.post("/")
async def speech_to_text(file: UploadFile = File(...)):
    """
    Accept an audio file and return its transcription using Whisper.
    Supports most audio formats via FFmpeg.
    """
    try:
        # Save uploaded file to a temporary location
        import tempfile, os
        suffix = os.path.splitext(file.filename)[1] or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            tmp.write(await file.read())

        # Transcribe audio
        text = transcribe_audio(tmp_path)

        # Cleanup
        os.remove(tmp_path)

        return {"transcription": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
