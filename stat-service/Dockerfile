FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8002

CMD uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload