from Tokenizer import Tokenizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

class TVT:
    def __init__(self, dataset):
        self.dataset = dataset
        self.tokenizer = Tokenizer()
        self.process()
        
    def process(self):
        # Preprocess reviews
        self.dataset['text'] = self.tokenizer.process(self.dataset['text'].tolist())
        
        # Encode sentiment labels
        self.dataset['sentiment'] = self.dataset['sentiment'].map({'positive': 1, 'negative': 0})
        
        # Split into train, validation, and test sets
        self.train_df, self.val_df, self.test_df = self._train_test_set()
        
        # Check balance
        self.check_dataset_balance(self.train_df, self.val_df, self.test_df)
        
        # Vectorize data using CountVectorizer and TF-IDF
        self.vectorizer, self.train_df_cv, self.val_df_cv, self.test_df_cv = self.count_vectorization(self.train_df, self.val_df, self.test_df)
        self.train_df_tfidf, self.val_df_tfidf, self.test_df_tfidf = self.TFIDF(self.train_df, self.val_df, self.test_df)

        
    def _train_test_set(self):
        # Split into train and temp sets
        train_df, temp_df = train_test_split(self.dataset, test_size=0.2, random_state=42)
        
        # Split temp set into validation and test sets
        val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)
        
        # Output sizes
        print(f"Train set size: {len(train_df)}")
        print(f"Validation set size: {len(val_df)}")
        print(f"Test set size: {len(test_df)}")
        
        return train_df, val_df, test_df
        
    def check_dataset_balance(self, train_df, val_df, test_df):
        def calculate_balance(df):
            total_count = len(df)
            positive_count = len(df[df['sentiment'] == 1])
            negative_count = len(df[df['sentiment'] == 0])
            positive_percentage = (positive_count / total_count) * 100 if total_count > 0 else 0
            negative_percentage = (negative_count / total_count) * 100 if total_count > 0 else 0
            return positive_percentage, negative_percentage

        train_pos, train_neg = calculate_balance(train_df)
        val_pos, val_neg = calculate_balance(val_df)
        test_pos, test_neg = calculate_balance(test_df)

        print("Train set balance:")
        print(f"Positive: {train_pos:.2f}%")
        print(f"Negative: {train_neg:.2f}%\n")

        print("Validation set balance:")
        print(f"Positive: {val_pos:.2f}%")
        print(f"Negative: {val_neg:.2f}%\n")

        print("Test set balance:")
        print(f"Positive: {test_pos:.2f}%")
        print(f"Negative: {test_neg:.2f}%")

    def count_vectorization(self, train_df, val_df, test_df):
        # Initialize CountVectorizer
        vectorizer = CountVectorizer(max_features=1000)
        
        # Fit and transform on train, transform on validation and test
        train_df_cv = vectorizer.fit_transform(train_df['text']).toarray()
        val_df_cv = vectorizer.transform(val_df['text']).toarray()
        test_df_cv = vectorizer.transform(test_df['text']).toarray()
        
        return vectorizer, train_df_cv, val_df_cv, test_df_cv

    def TFIDF(self, train_df, val_df, test_df):
        # Initialize TF-IDF vectorizer
        tfidf_vectorizer = TfidfVectorizer(max_features=1000)
        
        # Fit and transform on train, transform on validation and test
        train_df_tfidf = tfidf_vectorizer.fit_transform(train_df['text'])
        val_df_tfidf = tfidf_vectorizer.transform(val_df['text'])
        test_df_tfidf = tfidf_vectorizer.transform(test_df['text'])
        
        return train_df_tfidf, val_df_tfidf, test_df_tfidf

    def get_labels(self, type: str):
        train_labels = self.train_df['sentiment'].values
        val_labels = self.val_df['sentiment'].values
        test_labels = self.test_df['sentiment'].values
        
        if type == 'train':
            return train_labels
        elif type == 'val':
            return val_labels
        else:
            return test_labels
