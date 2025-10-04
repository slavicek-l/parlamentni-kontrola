FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/*


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md /app/

RUN pip install --upgrade pip && pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --only main --no-root

COPY . /app

# Explicitně nastav PYTHONPATH, aby byl modul 'app' vždy dosažitelný
ENV PYTHONPATH=/app

# Spouštěj exec formou, aby shell nepolykal chyby
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
