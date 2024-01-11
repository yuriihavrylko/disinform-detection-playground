from src.helpers.wandb_registry import download_model, publish_model
import textpruner
from transformers import (
    BertForSequenceClassification,
    BertTokenizer
)
from textpruner import summary, TransformerPruner


MODEL_ID = "yurii-havrylko/huggingface/bert_fake_news:v0"
MODEL_PATH = "/tmp/model"
PROJECT = "huggingface"


def load_model_and_tokenizer(model_path, tokenizer_name):
    model = BertForSequenceClassification.from_pretrained(model_path, local_files_only=True)
    tokenizer = BertTokenizer.from_pretrained(tokenizer_name)
    return model, tokenizer

def print_model_summary(model, message):
    print(message)
    print(summary(model))


def prune_bert_model(model):
    pruner = TransformerPruner(model)
    ffn_mask = textpruner.pruners.utils.random_mask_tensor((12,3072))
    head_mask = textpruner.pruners.utils.random_mask_tensor((12,12), even_masks=False)
    pruner.prune(head_mask=head_mask, ffn_mask=ffn_mask, save_model=True)
    return model


def print_pruned_model_info(model):
    for i in range(12):
        print ((model.base_model.encoder.layer[i].intermediate.dense.weight.shape,
                model.base_model.encoder.layer[i].intermediate.dense.bias.shape,
                model.base_model.encoder.layer[i].attention.self.key.weight.shape))


def test_inference_time(model, tokenizer, text):
    token = tokenizer(text, return_tensors="pt")
    inference_time = textpruner.inference_time(model, token)
    return inference_time

def main():
    model_path = "/tmp/model"
    pruned_model_path = "/tmp/pruned/model"
    tokenizer_name = "bert-base-uncased"
    text = "News title"

    download_model(MODEL_ID, PROJECT, model_path)

    model, tokenizer = load_model_and_tokenizer(model_path, tokenizer_name)

    print_model_summary(model, "Before pruning:")

    model = prune_bert_model(model)

    print_model_summary(model, "After pruning:")
    
    print_pruned_model_info(model)

    inference_time = test_inference_time(model, tokenizer, text)
    print(f"Inference time: {inference_time}")

    model.save_pretrained(pruned_model_path)
    tokenizer.save_pretrained(pruned_model_path)
    publish_model(pruned_model_path, PROJECT, "bert_fake_news_pruned")

if __name__ == "__main__":
    main()