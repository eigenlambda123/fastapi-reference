import whisper
from pydub import AudioSegment
import tempfile
import os

# Load Whisper model once
model = whisper.load_model("small")  #   can use "base", "small", "medium", "large"

def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio file to text using Whisper.
    Supports most formats via FFmpeg.
    """
    # Ensure audio is in WAV format for consistent processing
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        audio = AudioSegment.from_file(file_path)
        audio.export(tmp.name, format="wav")
        tmp_path = tmp.name

    # Transcribe
    result = model.transcribe(tmp_path)
    
    # Clean up temp file
    os.remove(tmp_path)

    return result["text"]
