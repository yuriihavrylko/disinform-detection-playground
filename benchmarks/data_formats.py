from datasets import load_dataset
import pandas as pd
import timeit
import os

dataset = load_dataset("inria-soda/tabular-benchmark", 'clf_cat_albert')

df = pd.DataFrame(dataset['train'])

file_formats = {
    'csv': {
        'write': lambda df: df.to_csv('sample.csv', index=False),
        'read': lambda: pd.read_csv('sample.csv')
    },
    'json': {
        'write': lambda df: df.to_json('sample.json', orient='records'),
        'read': lambda: pd.read_json('sample.json')
    },
    'parquet': {
        'write': lambda df: df.to_parquet('sample.parquet', index=False),
        'read': lambda: pd.read_parquet('sample.parquet')
    },
    'orc': {
        'write': lambda df: df.to_orc('sample.orc', index=False),
        'read': lambda: pd.read_orc('sample.orc')
    }
}

for format, methods in file_formats.items():
    print(f"Testing for {format.upper()} format:")
    
    write_time = timeit.timeit(lambda: methods['write'](df), number=10)
    read_time = timeit.timeit(methods['read'], number=10)
    
    write_file_size = os.path.getsize(f'sample.{format}') / (1024 * 1024)  # Convert bytes to MB
    
    print(f"Average time taken to write: {write_time / 10:.6f} seconds")
    print(f"Average time taken to read: {read_time / 10:.6f} seconds")
    print(f"File size after write: {write_file_size:.6f} MB")
    print("\n")
