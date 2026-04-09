FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/usr/local

COPY requirements.txt .

RUN uv pip install --no-cache --system -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
