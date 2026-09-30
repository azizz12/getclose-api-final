# Image de l'API FastAPI GetClose.
# Construite et lancée via : docker compose up -d --build

FROM python:3.12-slim

# Pas de fichiers .pyc, logs affichés immédiatement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances d'abord : Docker garde cette couche en cache tant que
# requirements.txt ne change pas, ce qui accélère les rebuilds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
