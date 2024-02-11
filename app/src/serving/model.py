from typing import List
import torch
from pathlib import Path
from filelock import FileLock
from transformers import (BertForSequenceClassification, BertTokenizer)
from torch.nn.functional import softmax
from src.helpers.wandb_registry import download_model


MODEL_ID = "yurii-havrylko/huggingface/bert_fake_news:v0"
MODEL_PATH = "/tmp/model"
MODEL_LOCK = ".lock-file"
PROJECT = "huggingface"

class BertPredictor:
    def __init__(self, model_load_path: str):
        self.tokenizer = BertTokenizer.from_pretrained(model_load_path)
        self.model = BertForSequenceClassification.from_pretrained(model_load_path)
        self.model.eval()
        self.labels = ['LABEL_0', 'LABEL_1']

    @torch.no_grad()
    def predict(self, text: List[str]):
        text_encoded = self.tokenizer.batch_encode_plus(list(text), return_tensors="pt", padding=True)
        bert_outputs = self.model(**text_encoded).logits
        probabilities = softmax(bert_outputs, dim=1)
        results = []
        for prob in probabilities:
            result = [{"label": self.labels[i], "score": float(score)} for i, score in enumerate(prob)]
            results.append(result)
        return results

    @classmethod
    def from_model_registry(cls) -> "BertPredictor":
        with FileLock(MODEL_LOCK):
            if not (Path(MODEL_PATH) / "model.safetensors").exists():
                download_model(model_name=MODEL_ID, download_path=MODEL_PATH, project=PROJECT)

        return cls(model_load_path=MODEL_PATH)

