FROM python:3.10-slim

WORKDIR /app

COPY analytics/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY analytics/ .

CMD ["python", "-m", "analytics"]