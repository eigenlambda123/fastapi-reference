from fastapi import APIRouter, HTTPException
from .schemas import TTSSchema
from .utils import text_to_speech_file, tts_file_response
from fastapi.responses import FileResponse

router = APIRouter(prefix="/tts", tags=["AI"])

@router.post("/", response_class=FileResponse)
async def tts_endpoint(request: TTSSchema):
    """
    Convert text to speech and return audio file.
    """
    try:
        file_path = text_to_speech_file(request.text, voice=request.voice, format=request.format)
        return tts_file_response(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
