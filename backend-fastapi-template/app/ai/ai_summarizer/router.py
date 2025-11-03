from fastapi import APIRouter, HTTPException, status
from .schemas import SummarizeRequest, SummarizeResponse
from .utils import summarize_text

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    """
    Summarize a given text using Cohere, with optional summary length control.
    """
    try:
        summary = await summarize_text(request.text, style=request.style or "medium")
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Summarization failed: {str(e)}",
        )
