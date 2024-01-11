import torch
from torch.nn import KLDivLoss, CrossEntropyLoss, Softmax
from transformers import (
    BertForSequenceClassification,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
    BertTokenizer,
    DataCollatorWithPadding
)
from datasets import load_dataset
from src.helpers.wandb_registry import download_model, publish_model

SEED = 42
MODEL_ID = "yurii-havrylko/huggingface/bert_fake_news:v0"
MODEL_PATH = "/tmp/model"
PROJECT = "huggingface"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_and_tokenize_data(tokenizer, split, shuffle=True, seed=SEED, max_length=512):
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding='max_length', truncation=True, max_length=max_length)
    
    dataset = load_dataset("GonzaloA/fake_news", split=split)
    if shuffle:
        dataset = dataset.shuffle(seed=seed)

    return dataset.map(tokenize_function, batched=True)

def initialize_models(teacher_checkpoint, student_pretrained):
    teacher = BertForSequenceClassification.from_pretrained(teacher_checkpoint, local_files_only=True).to(device)
    student = DistilBertForSequenceClassification.from_pretrained(student_pretrained).to(device)
    return teacher, student

def distillation_loss(teacher_logits, student_logits, temperature):
    softmax = Softmax(dim=1)
    kl_div = KLDivLoss(reduction="batchmean", log_target=True)
    soft_teacher_logits = softmax(teacher_logits / temperature)
    soft_student_logits = softmax(student_logits / temperature)
    return kl_div(soft_student_logits.log(), soft_teacher_logits)

class DistillationTrainer(Trainer):
    def __init__(self, teacher_model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.teacher_model = teacher_model

    def compute_loss(self, model, inputs, return_outputs=False):
        outputs = model(**inputs)
        student_logits = outputs.logits
        with torch.no_grad():
            teacher_outputs = self.teacher_model(**inputs)
            teacher_logits = teacher_outputs.logits
        loss_distillation = distillation_loss(teacher_logits, student_logits, temperature=2.0)
        labels = inputs.get("labels")
        criterion = CrossEntropyLoss()
        loss_ce = criterion(student_logits.view(-1, self.model.config.num_labels), labels.view(-1))
        alpha, T = 0.5, 2.0
        loss = alpha * loss_distillation * (T ** 2) + (1 - alpha) * loss_ce
        return (loss, outputs) if return_outputs else loss

def train_student_model(student, teacher, train_dataset, eval_dataset, tokenizer, training_args):
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    trainer = DistillationTrainer(
        teacher_model=teacher,
        model=student,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )
    trainer.train()
    return trainer.evaluate()

if __name__ == "__main__":
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    train_set = load_and_tokenize_data(tokenizer, "train[:10000]")
    valid_set = load_and_tokenize_data(tokenizer, "validation[:2000]")

    model_path = "/tmp/model"
    distil_model_path = "/tmp/distil/model"
    tokenizer_name = "bert-base-uncased"

    download_model(MODEL_ID, PROJECT, model_path)

    teacher, student = initialize_models(model_path, "distilbert-base-uncased")

    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=4,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=64,
        warmup_steps=100,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_strategy="epoch",
        evaluation_strategy="epoch"
    )

    eval_results = train_student_model(student, teacher, train_set, valid_set, tokenizer, training_args)
    print(f"Distillation Evaluation Results: {eval_results}")
    
    student.save_pretrained(distil_model_path)
    tokenizer.save_pretrained(distil_model_path)
    publish_model(distil_model_path, PROJECT, "bert_fake_news_distil")

