import pytest
from unittest.mock import MagicMock, create_autospec
from transformers import BertTokenizer, BertForSequenceClassification, Trainer
from src.model.training import load_data, tokenize_data, prepare_datasets, train_model, MODEL_NAME

@pytest.fixture
def mock_dataset(monkeypatch):
    dataset_mock = create_autospec(spec={
        "train": MagicMock()
    }, instance=True)

    dataset_mock['train'].shuffle.return_value = dataset_mock['train']

    dataset_mock['train'].select.return_value = {
        'input_ids': [[101, 102], [202, 203]],
        'attention_mask': [[1, 1], [1, 1]],
        'labels': [0, 1]
    }

    monkeypatch.setattr("src.model.training.load_dataset", MagicMock(return_value=dataset_mock))
    return dataset_mock

@pytest.fixture
def mock_tokenizer():
    tokenizer = create_autospec(BertTokenizer.from_pretrained('bert-base-uncased'))
    tokenizer.encode_plus.return_value = {
        'input_ids': [101, 102],
        'attention_mask': [1, 1]
    }
    tokenizer.__call__ = tokenizer.encode_plus
    return tokenizer

def test_load_data(monkeypatch, mock_dataset):
    monkeypatch.setattr("src.model.training.wandb.log", MagicMock())
    dataset = load_data()
    assert dataset is not None

def test_tokenize_data(monkeypatch, mock_dataset, mock_tokenizer):
    mock_dataset['train'].map.return_value = mock_dataset['train']
    tokenized_dataset = tokenize_data(mock_tokenizer, mock_dataset['train'])
    mock_dataset['train'].map.assert_called()

def test_prepare_datasets(mock_dataset):
    args = MagicMock()
    args.train_size = 1
    args.eval_size = 1
    
    mock_dataset['train'].select.side_effect = [
        {'labels': [0], 'input_ids': [[101, 102]], 'attention_mask': [[1, 1]]},
        {'labels': [1], 'input_ids': [[202, 203]], 'attention_mask': [[1, 1]]}
    ]
    
    train_dataset, eval_dataset = prepare_datasets(mock_dataset['train'], args)
    assert train_dataset['labels'] == [0]
    assert eval_dataset['labels'] == [1]

def test_train_model(monkeypatch, mock_dataset, mock_tokenizer):
    model = create_autospec(BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2))
    args = MagicMock()
    train_dataset = mock_dataset['train'].select(1)
    eval_dataset = mock_dataset['train'].select(1)

    mock_trainer = create_autospec(Trainer)
    monkeypatch.setattr("src.model.training.Trainer", mock_trainer)
    
    train_model(model, mock_tokenizer, train_dataset, eval_dataset)
    assert mock_trainer.called
