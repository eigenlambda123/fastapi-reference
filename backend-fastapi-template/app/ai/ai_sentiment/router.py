from fastapi import APIRouter, HTTPException, status
from .schemas import SentimentRequest, SentimentResponse
from .utils import analyze_sentiment

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/sentiment", response_model=SentimentResponse)
async def sentiment_analysis(request: SentimentRequest):
    """
    Analyze the sentiment of a given text.
    """
    try:
        result = await analyze_sentiment(request.text)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
