from pydantic import ValidationError
from fastapi import HTTPException
from sentiment.models import (
    SentimentRequest,
    SentimentRespone,
    PageSummary,
    PageComparison,
)
from sentiment.fetch import fetch_data
from sentiment.nlp import compute, from_body
from fastapi import routing
from sentiment.config import nlp
import logging

logger = logging.getLogger(__name__)


router = routing.APIRouter()


@router.post(
    "/linguistic-analysis-semantic-comparison", response_model=SentimentRespone
)
async def read_root(sentiment_request: SentimentRequest):
    if len(sentiment_request.urls) < 1:
        raise HTTPException(status_code=400, detail="Provide at least one URL")
    try:
        data = await fetch_data(sentiment_request.urls)
        data = [(url, from_body(text)) for url, text in data]
        summaries, similarities = compute(nlp[sentiment_request.localization], data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    try:
        nouns = [PageSummary(**summary) for summary in summaries]
        similarities_ = [PageComparison(**similarity) for similarity in similarities]
        response = SentimentRespone(nouns=nouns, similarities=similarities_)
    except ValidationError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    response.sort_similarities()
    response.cutoff_similarities()
    return response
