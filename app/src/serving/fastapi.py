from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from src.serving.model import BertPredictor


class Payload(BaseModel):
    text: List[str]


app = FastAPI()
predictor = BertPredictor.from_model_registry()


@app.post("/predict")
def predict(payload: Payload):
    prediction = predictor.predict(text=payload.text)
    return prediction
