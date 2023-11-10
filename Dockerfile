FROM python:3.12-slim as builder

WORKDIR /app

COPY app/requirements.txt .
RUN pip install -r requirements.txt

FROM builder

COPY app .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
EXPOSE 8000
