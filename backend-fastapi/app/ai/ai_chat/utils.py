import cohere
from app.core.config import settings
from .prompts import PRESET_PROMPTS
from app.core.cache import cached

co = cohere.Client(settings.COHERE_API_KEY)

@cached(ttl=300)
def generate_chat_response(messages, model="command-r-plus", temperature=0.5, system_prompt=None, preset=None):
    """
    Generate a chat response from Cohere with optional system prompt or preset.
    """

    # Determine which prompt to use
    if preset and preset in PRESET_PROMPTS:
        system_prompt = PRESET_PROMPTS[preset]
    elif not system_prompt:
        system_prompt = PRESET_PROMPTS["default"]

    formatted_messages = []

    # Add user messages as proper history
    for msg in messages[:-1]:  
        formatted_messages.append({
            "role": msg.role,
            "message": msg.content
        })

    # Extract the final user message separately
    last_message = messages[-1].content

    # Send chat request
    response = co.chat(
        model=model,
        message=last_message,
        chat_history=formatted_messages,  
        temperature=temperature,
        preamble=system_prompt, 
    )

    return response.text.strip()
