import tempfile
from pathlib import Path
from fastapi.responses import FileResponse

# Example using pyttsx3 for offline TTS
import pyttsx3

def text_to_speech_file(text: str, voice: str = "alloy", format: str = "mp3") -> Path:
    """
    Convert text to speech and return a file path.
    """
    engine = pyttsx3.init()
    
    # Choose voice if available
    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)
    
    # Create temporary file
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}")
    tmp_file.close()

    # Save audio to file
    engine.save_to_file(text, tmp_file.name)
    engine.runAndWait()

    return Path(tmp_file.name)

def tts_file_response(file_path: Path):
    """
    Return a FastAPI FileResponse for the generated TTS file.
    """
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg" if file_path.suffix == ".mp3" else "audio/wav",
        filename=file_path.name
    )
