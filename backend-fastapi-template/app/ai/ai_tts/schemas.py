from pydantic import BaseModel

class TTSSchema(BaseModel):
    text: str
    voice: str = "alloy"      # Example: "alloy", "verse"
    format: str = "mp3"       # "mp3" or "wav"
