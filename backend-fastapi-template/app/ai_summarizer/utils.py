import cohere
from app.core.config import settings    

co = cohere.Client(settings.COHERE_API_KEY)

async def summarize_text(text: str, style: str = "medium") -> str:
    if style == "short":
        instruction = "Summarize in 1–2 sentences."
    elif style == "long":
        instruction = "Summarize in 2–3 short paragraphs, covering context and details."
    else:
        instruction = "Summarize in one concise paragraph."
    
    response = co.chat(
        model="command-a-03-2025",
        message=f"{instruction}\n\n{text}",
        temperature=0.3,
    )

    return response.text.strip()
