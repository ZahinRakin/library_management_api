FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8003

CMD uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload