from TVT import TVT
from SentimentModel import SentimentModel
import pandas as pd

class SentimentAnalyzer:
    def __init__(self, dataset: pd.DataFrame):
        self._dataset = dataset
        self._tvt = TVT(dataset)
        self._model = SentimentModel(self._tvt.train_df_cv.shape[1])
        self._train_model()
        self._test_model(show_result=True)    
    
    def isPositive(self, statement):
        statement = self._tvt.vectorizer.transform([statement])
        prediction = self._model.predict(statement)[0][0]
        print(prediction)
        return True if prediction >= 0.5 else False
    
    def get_sentiment_value(self, statement):
        statement = self._tvt.vectorizer.transform([statement])
        prediction = self._model.predict(statement)[0][0]
        return prediction
        
    def _train_model(self):
        self._model.train(self._tvt.train_df_cv, self._tvt.get_labels('train'), self._tvt.val_df_cv, self._tvt.get_labels('val'), epochs=5)
    
    def _test_model(self, show_result=False):
        test_loss, test_accuracy = self._model.evaluate(self._tvt.test_df_cv, self._tvt.get_labels('test'))
        if (show_result):
            print(f"Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy:.4f}")

