from pydantic import BaseModel, Field

class SentimentRequest(BaseModel):
    text: str = Field(..., example="I love how intuitive this app is!")

class SentimentResponse(BaseModel):
    sentiment: str = Field(..., example="positive")
    confidence: float = Field(..., example=0.92)
