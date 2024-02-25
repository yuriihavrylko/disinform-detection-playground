FROM python:3.8-slim

WORKDIR /app
ADD . /app
ENV PYTHONUNBUFFERED 1

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r app/requirements-dev.txt

# Run the command to start the model training
CMD ["python", "app/model/training.py"]
