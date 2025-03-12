from pydantic_settings import BaseSettings

nlp = {}


class Settings(BaseSettings):
    MOST_COMMON_NOUNS_COUNT: int = 50
    SIMILARITY_THRESHOLD: float = 0.5


settings = Settings()
