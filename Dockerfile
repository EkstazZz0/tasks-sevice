FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev

WORKDIR /api

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tests ./tests
COPY pytest.ini .

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

ENTRYPOINT ["uvicorn", "app.main:app"]