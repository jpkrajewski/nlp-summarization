from typing import Dict, List
from pydantic import BaseModel, HttpUrl

from sentiment.config import config
import logging

logger = logging.getLogger(__name__)


class SentimentRequest(BaseModel):
    urls: List[HttpUrl]
    localization: str = "en"


class PageSummary(BaseModel):
    url: str
    nouns: Dict[str, int]


class PageComparison(BaseModel):
    url_1: str
    url_2: str
    score: float


class SentimentRespone(BaseModel):
    nouns: List[PageSummary]
    similarities: List[PageComparison]

    def sort_similarities(self):
        self.similarities.sort(key=lambda x: x.score, reverse=True)

    def cutoff_similarities(self):
        self.similarities = [
            sim for sim in self.similarities if sim.score >= config.SIMILARITY_THRESHOLD
        ]
