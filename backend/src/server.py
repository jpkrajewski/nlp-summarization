from contextlib import asynccontextmanager
from fastapi import FastAPI
import spacy
from src.main import router
from src.config import nlp


@asynccontextmanager
async def lifespan(app: FastAPI):
    nlp["en"] = spacy.load("en_core_web_sm")
    nlp["pl"] = spacy.load("pl_core_news_sm")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
