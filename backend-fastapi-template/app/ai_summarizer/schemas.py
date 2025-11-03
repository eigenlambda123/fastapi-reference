from pydantic import BaseModel, Field
from typing import Literal

class SummarizeRequest(BaseModel):
    text: str = Field(..., description="The text to summarize.")
    style: Literal["short", "medium", "long"] = Field("medium", description="Summary length style.")

class SummarizeResponse(BaseModel):
    summary: str
