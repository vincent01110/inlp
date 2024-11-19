import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import string

from Tokenizer import Tokenizer



# Example: Scraping sports articles from a website
url = 'https://example.com/sports-news'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extracting text from the articles
articles = []
for article in soup.find_all('article'):
    title = article.find('h2').text
    content = article.find('p').text
    articles.append({'title': title, 'content': content})



nltk.download('punkt')

def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Preprocess articles
for article in articles:
    article['processed_content'] = preprocess_text(article['content'])


for article in articles:
    article['sentences'] = sent_tokenize(article['content'])


from collections import Counter

def get_word_frequencies(text):
    words = word_tokenize(text)
    return Counter(words)

# Calculate word frequencies for each article
for article in articles:
    word_freq = get_word_frequencies(article['processed_content'])
    article['word_frequencies'] = word_freq


def score_sentences(sentences, word_frequencies):
    sentence_scores = {}
    
    for sentence in sentences:
        sentence_word_count = len(word_tokenize(sentence))
        for word in word_tokenize(sentence):
            if word in word_frequencies:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word] / sentence_word_count
                else:
                    sentence_scores[sentence] += word_frequencies[word] / sentence_word_count

    return sentence_scores

# Score sentences for each article
for article in articles:
    article['sentence_scores'] = score_sentences(article['sentences'], article['word_frequencies'])


def get_summary(sentences, sentence_scores, top_n=3):
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    return ' '.join(ranked_sentences[:top_n])

# Generate summaries for each article
for article in articles:
    article['summary'] = get_summary(article['sentences'], article['sentence_scores'], top_n=3)

# Print the summaries
for article in articles:
    print("Title:", article['title'])
    print("Summary:", article['summary'])
    print("\n")
