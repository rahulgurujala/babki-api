FROM python:3.11-slim-bullseye

WORKDIR /denarii

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY . .

CMD uvicorn app.main:app --host=0.0.0.0 --port=8000 --reload
