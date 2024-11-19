import pandas as pd
from utils import rename_dataset_columns
from SentimentAnalyzer import SentimentAnalyzer


imdb_dataset = pd.read_csv("hf://datasets/scikit-learn/imdb/IMDB Dataset.csv")
imdb_dataset = imdb_dataset.rename(columns={'review':'text'})
print(imdb_dataset.head())

analyzer = SentimentAnalyzer(imdb_dataset)
print(analyzer.isPositive(''))