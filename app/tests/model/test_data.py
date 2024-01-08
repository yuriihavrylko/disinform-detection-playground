import pytest
from datasets import load_dataset
from great_expectations.data_context import DataContext
from great_expectations.dataset import PandasDataset

DATASET_NAME = "GonzaloA/fake_news"

@pytest.fixture(scope="session")
def huggingface_dataset():
    dataset = load_dataset(DATASET_NAME, split="train")
    df = dataset.to_pandas()
    ge_dataset = PandasDataset(df)
    return ge_dataset

def test_huggingface_dataset_with_great_expectations(huggingface_dataset):
    assert huggingface_dataset.shape[0] == 24353

    assert huggingface_dataset.expect_column_values_to_not_be_null(column="label")["success"]
    assert huggingface_dataset.expect_column_values_to_not_be_null(column="title")["success"]
    assert huggingface_dataset.expect_column_values_to_not_be_null(column="text")["success"]

    assert huggingface_dataset.expect_column_values_to_be_unique(column="text")["success"]

    assert huggingface_dataset.expect_column_values_to_be_in_set("label", [1, 0])["success"]
