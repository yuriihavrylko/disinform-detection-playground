---
language: en
tags:
- bert
license: apache-2.0
datasets:
- GonzaloA/fake_news
---

# BERT fake news classifiction model

Pretrained model on English language based on uncased version of BERT finetuned for task of binary classification.


### How to use

You can use this model directly with a pipeline for masked language modeling:

```python

tokenizer = BertTokenizer.from_pretrained(PATH, local_files_only=True)
bert_model = BertForSequenceClassification.from_pretrained(PATH, local_files_only=True)

# run infernce 

```
With transformers pipeline

```python

text_classification_pipeline = pipeline(
    "text-classification",
    model=PATH,
    tokenizer=PATH,
    return_all_scores=True
)
```


## Training data

The BERT model was pretrained on [bert-base-uncased](https://huggingface.co/bert-base-uncased), a dataset consisting of ~25,000 of news labeled as fake and real.
For training purpoose 10k of samples randomly selected and splitted in 80:20 ratio.

## Training procedure

### Preprocessing

The texts are tokenized using BERT tokenizer.

### Training

The model was trained on GPU T4 x 2.

## Evaluation results


| Epoch | Training Loss | Validation Loss | Accuracy |
|-------|---------------|-----------------|----------|
| 1     | 0.074000      | 0.027787        | 0.986500 |
| 2     | 0.032600      | 0.010920        | 0.995000 |
| 3     | 0.010100      | 0.002739        | 0.999500 |

