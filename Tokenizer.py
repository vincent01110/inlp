import re
from bs4 import BeautifulSoup
import contractions
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class Tokenizer:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('punkt_tab')

    def process(self, data: list) -> list:
        """Processes the input data through various cleaning steps."""
        data = [self._remove_extra_whitespace(entry) for entry in data]
        data = [self._remove_special_characters(entry) for entry in data]
        data = [self._remove_html_tags(entry) for entry in data]
        data = [self._expand_contractions(entry) for entry in data]
        data = [self._remove_punctuation(entry) for entry in data]
        data = [self._remove_numbers(entry) for entry in data]
        data = [self._remove_stopwords(entry) for entry in data]
        data = [self._lemmatize_text(entry) for entry in data]
        return data

    def _remove_extra_whitespace(self, text: str) -> str:
        """Removes leading/trailing whitespace and replaces multiple spaces with a single space."""
        text = text.strip()
        text = " ".join(text.split())
        return text

    def _remove_special_characters(self, text: str) -> str:
        """Removes special characters from the text."""
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        return text

    def _remove_html_tags(self, text: str) -> str:
        """Removes HTML tags from the text."""
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

    def _expand_contractions(self, text: str) -> str:
        """Expands contractions in the text."""
        return contractions.fix(text)

    def _remove_punctuation(self, text: str) -> str:
        """Removes punctuation from a string."""
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)

    def _remove_numbers(self, text: str) -> str:
        """Removes numbers from a string."""
        result = ''.join([i for i in text if not i.isdigit()])
        return result

    def _remove_stopwords(self, text: str) -> str:
        """Removes stopwords from a string."""
        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w.lower() in self.stop_words]
        return " ".join(filtered_sentence)

    def _lemmatize_text(self, text: str) -> str:
        """Lemmatizes words in a string."""
        word_tokens = word_tokenize(text)
        lemmatized_sentence = [self.lemmatizer.lemmatize(w) for w in word_tokens]
        return " ".join(lemmatized_sentence)

