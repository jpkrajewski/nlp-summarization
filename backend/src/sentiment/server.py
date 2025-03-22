from contextlib import asynccontextmanager
import logging
from logging import config as logging_config
from fastapi import FastAPI
from sentiment.config import config
import spacy
from sentiment.main import router
from sentiment.config import nlp


@asynccontextmanager
async def lifespan(app: FastAPI):
    nlp["en"] = spacy.load("en_core_web_sm")
    nlp["pl"] = spacy.load("pl_core_news_sm")
    yield


def configure_logger() -> None:
    cmt_logger = logging.getLogger(__name__)
    logging_config.fileConfig(config.LOGGING_CONF_PATH, disable_existing_loggers=False)
    cmt_logger.info(config)


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    configure_logger()
    return app


app = create_app()
