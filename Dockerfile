FROM python:3.12-slim as builder

WORKDIR /app

COPY app/requirements.txt .
RUN pip install -r requirements.txt

FROM builder AS app-flask

COPY app .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
EXPOSE 8000

FROM base AS app-streamlit
CMD streamlit run --server.address 0.0.0.0 --server.port 8080 src/serving/streamlit.py


FROM base AS app-fastapi
CMD uvicorn --host 0.0.0.0 --port 8090 --workers 4 src.serving.fastapi:app 
