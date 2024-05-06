FROM python:3.11-slim

WORKDIR /fastapi_med

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD uvicorn itmed:app --host 0.0.0.0 --port 8000
