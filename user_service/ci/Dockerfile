FROM python:3.10-alpine

RUN mkdir -p /src/app

WORKDIR /src/app
ENV PYTHONUNBUFFERED=1

RUN apk update && \
    apk upgrade

COPY src/requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

CMD uvicorn app:app --reload --host 0.0.0.0 --port 8001
EXPOSE 8001