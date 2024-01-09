import argparse
import numpy as np
from datasets import load_dataset
from transformers import (BertForSequenceClassification, BertTokenizer, TrainingArguments, Trainer)
from transformers import DataCollatorWithPadding
import evaluate
import wandb

MODEL_NAME = "bert-base-uncased"
SEED = 42
TRAIN_SIZE = 8000
EVAL_SIZE = 2000
DATASET_NAME = "GonzaloA/fake_news"

def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Train BERT for sequence classification.")
    parser.add_argument('--train_size', type=int, default=TRAIN_SIZE,
                        help='Number of samples to use for training')
    parser.add_argument('--eval_size', type=int, default=EVAL_SIZE,
                        help='Number of samples to use for evaluation')
    return parser.parse_args(args=None)

def load_data(dataset_name=DATASET_NAME):
    """Loads a dataset using Huggingface's datasets library."""
    dataset = load_dataset(dataset_name)

    wandb.log({"dataset": dataset_name})
    
    return dataset

def tokenize_data(tokenizer, dataset, padding=True, truncation=True, max_length=512):
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding=padding, truncation=truncation, max_length=max_length)
    
    return dataset.map(tokenize_function, batched=True)

def configure_training_args(output_dir="test_trainer"):
    """Sets up the training arguments for the Trainer."""
    return TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_dir=f"{output_dir}/logs",  # directory for storing logs
        logging_steps=10,
        seed=SEED,
    )

def compute_metrics(eval_pred):
    """Computes accuracy of the model predictions."""
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return evaluate.load("accuracy").compute(predictions=predictions, references=labels)

def prepare_datasets(tokenized_datasets, args):
    """Prepare the training and evaluation datasets from tokenized data."""
    train_dataset = tokenized_datasets.select(range(args.train_size))
    eval_dataset = tokenized_datasets.select(range(args.train_size, args.train_size + args.eval_size))
    return train_dataset, eval_dataset

def train_model(model, tokenizer, train_dataset, eval_dataset):
    """Initialize the Trainer and train the model."""
    training_args = configure_training_args()
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics,
        data_collator=data_collator,
    )

    trainer.train()
    return trainer

def initialize_wandb(args):
    """Initialize Weights & Biases."""
    wandb.init(project="bert_fake_news_classification", entity="your_wandb_username", config=args)

def save_model_and_tokenizer(trainer, tokenizer, path="./model_checkpoint"):
    """Save the trained model and tokenizer."""
    trainer.save_model(path)
    tokenizer.save_pretrained(path)
    return path

def log_to_wandb(dataset_name, artifact_path):
    """Log dataset and model artifact to Weights & Biases."""
    wandb.log({"dataset": dataset_name})
    wandb.log_artifact(artifact_path, type="model", name="bert_fake_news_classifier")

def finish_wandb():
    """Finish the Weights & Biases run."""
    wandb.finish()

def load_and_preprocess_data(train_size=TRAIN_SIZE, eval_size=EVAL_SIZE):
    datasets = load_data()
    small_train_dataset = datasets["train"].shuffle(seed=SEED).select(range(train_size + eval_size))
    return small_train_dataset

def prepare_model_and_tokenizer():
    model = BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    return model, tokenizer

def tokenize_datasets(tokenizer, small_train_dataset):
    tokenized_datasets = tokenize_data(tokenizer, small_train_dataset)
    tokenized_datasets = tokenized_datasets.remove_columns(["text"])
    return tokenized_datasets

def split_datasets(tokenized_datasets, args):
    return prepare_datasets(tokenized_datasets, args)

def perform_training(model, tokenizer, train_dataset, eval_dataset):
    return train_model(model, tokenizer, train_dataset, eval_dataset)

def save_and_log_artifacts(trainer, tokenizer):
    artifact_path = save_model_and_tokenizer(trainer, tokenizer)
    log_to_wandb(DATASET_NAME, artifact_path)


# The main function now orchestrates the calls to the decoupled parts
def main():
    args = parse_args()
    initialize_wandb(args)

    small_train_dataset = load_and_preprocess_data(args.train_size, args.eval_size)

    model, tokenizer = prepare_model_and_tokenizer()

    tokenized_datasets = tokenize_datasets(tokenizer, small_train_dataset)
    
    train_dataset, eval_dataset = split_datasets(tokenized_datasets, args)

    trainer = perform_training(model, tokenizer, train_dataset, eval_dataset)

    save_and_log_artifacts(trainer, tokenizer)

    finish_wandb()

if __name__ == "__main__":
    main()
