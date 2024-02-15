import pandas as pd
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import EmbeddingsDriftMetric
from evidently.metrics.data_drift.embedding_drift_methods import distance
from sentence_transformers import SentenceTransformer

from src.model.training import load_data


def create_embeddings(model, texts, batch_size=32):
    embeddings = model.encode(texts, batch_size=batch_size)
    return embeddings

def prepare_dataframe(dataset, embeddings):
    df = pd.DataFrame(dataset[:10000])
    embeddings_df = pd.DataFrame(embeddings, index=df.index)
    df = pd.concat([df, embeddings_df], axis=1)
    return df

def generate_report(df, column_mapping):
    report = Report(metrics=[
        EmbeddingsDriftMetric('small_subset', 
                              drift_method=distance(
                                  dist='cosine',
                                  threshold=0.2,
                                  pca_components=None,
                                  bootstrap=None,
                                  quantile_probability=0.95
                              )
                             )
    ])
    report.run(reference_data=df[:2000], current_data=df[2000:], column_mapping=column_mapping)
    return report

def main():
    model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L12-v2')
    
    ds = load_data()
    
    embeddings = create_embeddings(model, ds['text'])
    
    df = prepare_dataframe(ds, embeddings)
    
    column_mapping = ColumnMapping(
        embeddings={'small_subset': df.columns[4:]}
    )
    
    report = generate_report(df, column_mapping)
    
    report.show(mode='inline')

if __name__ == "__main__":
    main()
     
