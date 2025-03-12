## How to start

### Docker
```bash
docker compose up --build
```

### Local

```bash
cd backend
uv venv
source venv/bin/activate
uv pip install -e .

uv pip install pip
uv run --with spacy spacy download pl_core_news_sm
uv run --with spacy spacy download en_core_web_sm

fastapi dev src/server.py
```

UV provides the PIP interface, but the spacy models are downloaded using native PIP that is why the `uv pip install pip` is needed.