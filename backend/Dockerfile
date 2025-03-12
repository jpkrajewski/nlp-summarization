FROM python:3.12-slim-bookworm 

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VIRTUAL_ENV="/venv"

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m venv $VIRTUAL_ENV

WORKDIR /app

ENV PYTHONPATH="/app:$PYTHONPATH"

COPY pyproject.toml ./

COPY src/ ./src

RUN pip install -e .

RUN python -m spacy download pl_core_news_sm
RUN python -m spacy download en_core_web_sm

EXPOSE 8000

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]