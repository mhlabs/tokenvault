FROM python:3.9.6-slim
#FROM python:3.10-slim-bullseye

WORKDIR /api
COPY . /api

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD exec gunicorn \
    --bind :$PORT \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --threads 8 \
    --timeout 0 \
    tokenvaultapi.main:api