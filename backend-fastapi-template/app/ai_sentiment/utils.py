import cohere
import json
import ast
import re
from app.core.config import settings
from typing import Dict, Any

co = cohere.Client(settings.COHERE_API_KEY)

def _extract_first_json(text: str) -> str | None:
    """
    Extract the first balanced JSON object from text.
    Returns the JSON substring (including braces) or None if not found.
    This finds the first '{' and then looks for the matching '}' using a stack.
    """
    start = text.find("{")
    if start == -1:
        return None

    stack = []
    for i in range(start, len(text)):
        ch = text[i]
        if ch == "{":
            stack.append("{")
        elif ch == "}":
            if stack:
                stack.pop()
                if not stack:
                    return text[start : i + 1]
    return None

def _safe_parse_json(maybe_json: str) -> Dict[str, Any] | None:
    """
    Try json.loads, then fallback to ast.literal_eval for single-quoted dicts.
    Returns a dict or None.
    """
    try:
        return json.loads(maybe_json)
    except Exception:
        try:
            # ast.literal_eval can parse Python dicts with single quotes
            return ast.literal_eval(maybe_json)
        except Exception:
            return None

async def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment using Cohere's chat API.
    Returns {'sentiment': 'positive'|'negative'|'neutral'|'unknown', 'confidence': float}
    """
    # Strong instruction to return ONLY JSON
    prompt = (
        "You are a sentiment classifier. Classify the following text as Positive, Negative, or Neutral\n"
        "and return ONLY a single JSON object with keys `sentiment` and `confidence`.\n"
        "Example:\n"
        '{"sentiment":"positive","confidence":0.93}\n\n'
        f"Text: {text}"
    )

    # Lower temperature to reduce hallucinations
    response = co.chat(
        model="command-a-03-2025",
        message=prompt,
        temperature=0.0,  # deterministic
    )

    raw = response.text or ""
    # helpful for debugging — remove or route to logger in production
    print("Cohere raw response:", repr(raw))

    # try to parse the whole text as JSON directly
    parsed = None
    try:
        parsed = json.loads(raw.strip())
    except Exception:
        # try to extract first {...} block
        maybe = _extract_first_json(raw)
        if maybe:
            parsed = _safe_parse_json(maybe)

    # last-resort heuristics: try to find keywords and approximate confidence
    if parsed is None:
        # simple heuristic fallback
        lower = raw.lower()
        if "positive" in lower:
            sentiment = "positive"
        elif "negative" in lower:
            sentiment = "negative"
        elif "neutral" in lower:
            sentiment = "neutral"
        else:
            sentiment = "unknown"
        # fallback confidence: try to parse percent or number in text
        conf_match = re.search(r"([01](?:\.\d+)|0?\.\d+|\d{1,3}%?)", raw)
        confidence = 0.0
        if conf_match:
            val = conf_match.group(1)
            try:
                if val.endswith("%"):
                    confidence = float(val[:-1]) / 100.0
                else:
                    confidence = float(val)
                    if confidence > 1:
                        confidence = min(confidence / 100.0, 1.0)
            except Exception:
                confidence = 0.0

        return {"sentiment": sentiment, "confidence": round(confidence, 3)}

    # Normalize parsed output
    sentiment = parsed.get("sentiment") if isinstance(parsed.get("sentiment"), str) else None
    confidence = parsed.get("confidence")
    if sentiment:
        sentiment = sentiment.lower()
        if sentiment not in ("positive", "negative", "neutral"):
            sentiment = "unknown"
    else:
        sentiment = "unknown"

    try:
        confidence = float(confidence)
        if confidence > 1:
            # if model returned 93, interpret as 0.93
            confidence = min(confidence / 100.0, 1.0)
        confidence = max(0.0, min(confidence, 1.0))
    except Exception:
        confidence = 0.0

    return {"sentiment": sentiment, "confidence": round(confidence, 3)}
