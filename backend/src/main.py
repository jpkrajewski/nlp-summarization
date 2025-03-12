from fastapi import HTTPException
from src.models import SentimentRequest, SentimentRespone
from src.fetch import fetch_data
from src.nlp import compute, from_body
from fastapi import routing
from src.config import nlp
import logging

logger = logging.getLogger(__name__)


router = routing.APIRouter()


@router.post(
    "/linguistic-analysis-semantic-comparison", response_model=SentimentRespone
)
async def read_root(sentiment_request: SentimentRequest):
    if len(sentiment_request.urls) < 1:
        raise HTTPException(status_code=400, detail="Provide at least one URL")
    data = await fetch_data(sentiment_request.urls)
    data = [(url, from_body(text)) for url, text in data]
    summaries, similarities = compute(nlp[sentiment_request.localization], data)
    response = SentimentRespone(nouns=summaries, similarities=similarities)
    response.sort_similarities()
    response.cutoff_similarities()
    return response
