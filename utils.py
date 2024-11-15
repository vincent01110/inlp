import pandas as pd


def rename_dataset_columns(dataset: pd.DataFrame, columns: dict):
    dataset.rename(columns)
    return dataset