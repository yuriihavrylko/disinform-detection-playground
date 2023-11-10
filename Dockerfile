FROM python:3.12-slim as builder

WORKDIR /app

FROM builder

EXPOSE 8000
