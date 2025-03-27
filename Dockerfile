FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

ENV POETRY_VIRTUALENVS_CREATE=false
RUN python3 -m pip install --upgrade pip \
 && python3 -m pip install poetry \
 && python3 -m poetry install --no-root

COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH='/app'

CMD ["python3", "quiz_bot/bot/main.py"]