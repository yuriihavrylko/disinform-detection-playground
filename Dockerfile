FROM python:3.11-slim as builder

WORKDIR /app

COPY app/requirements.txt .
RUN pip install -r requirements.txt

FROM builder AS app-flask

COPY app .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
EXPOSE 8000

FROM builder AS app-streamlit
CMD streamlit run --server.address 0.0.0.0 --server.port 8080 src/serving/streamlit.py


FROM builder AS app-fastapi
CMD uvicorn --host 0.0.0.0 --port 8090 --workers 4 src.serving.fastapi:app 

FROM builder AS app-seldon
EXPOSE 5000
EXPOSE 9000
ENV MODEL_NAME SeldonAPI
ENV SERVICE_TYPE MODEL
COPY app/src/serving/seldon.py /app/SeldonAPI.py

RUN chown -R 8888 /app
RUN mkdir /.cache
RUN chmod 777 /.cache
RUN mkdir /.config
RUN chmod 777 /.config

CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE

FROM builder AS app-kserve
ENTRYPOINT ["python", "app/src/serving/kserve.py"]
