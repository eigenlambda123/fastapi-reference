import cohere
from app.core.config import settings
from .prompts import PRESET_PROMPTS
from app.core.cache import cached

co = cohere.Client(settings.COHERE_API_KEY)

role_map = {
    "user": "User",
    "assistant": "Chatbot",
    "system": "System",
    "tool": "Tool"
}

@cached(ttl=300)
def generate_chat_response(messages, model, temperature=0.5, system_prompt=None, preset=None):
    """
    Generate a chat response from Cohere with optional system prompt or preset.
    Uses the last user message as the prompt, and all previous messages as history.
    """

    # Determine which prompt to use
    if preset and preset in PRESET_PROMPTS:
        system_prompt = PRESET_PROMPTS[preset]
    elif not system_prompt:
        system_prompt = PRESET_PROMPTS["default"]

    # Find the last user message
    last_user_idx = None
    for i in reversed(range(len(messages))):
        if messages[i].role == "user":
            last_user_idx = i
            break
    if last_user_idx is None:
        raise ValueError("No user message found.")

    last_message = messages[last_user_idx].content
    formatted_messages = [
        {
            "role": role_map.get(msg.role, msg.role),
            "message": msg.content
        }
        for msg in messages[:last_user_idx]
    ]

    try:
        response = co.chat(
            model=model,
            message=last_message,
            chat_history=formatted_messages,
            temperature=temperature,
            preamble=system_prompt,
        )
        return response.text.strip()
    except Exception as e:
        print("Cohere error:", e)
        raise
