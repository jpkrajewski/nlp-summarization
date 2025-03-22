from pathlib import Path
from pydantic_settings import BaseSettings

nlp = {}
LOGGING_CONF_DIR: Path = Path(__file__).parents[0] / "logging"


class Config(BaseSettings):
    MOST_COMMON_NOUNS_COUNT: int = 50
    SIMILARITY_THRESHOLD: float = 0.5
    LOGGING_CONF_PATH: Path = LOGGING_CONF_DIR / "logging_dev.conf"


config = Config()
