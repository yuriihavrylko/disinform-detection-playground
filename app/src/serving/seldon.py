import logging

from src.serving.model import BertPredictor

logger = logging.getLogger()


class SeldonAPI:
    def __init__(self):
        self.predictor = BertPredictor.from_model_registry()

    def predict(self, text):
        logger.info(text)
        results = self.predictor.predict(text)
        logger.info(results)
        return results
