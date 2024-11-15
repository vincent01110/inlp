import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from transformers import BertTokenizer
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, concatenate
from transformers import TFBertModel

# Load your CSV file
data = pd.read_csv('your_articles.csv')

# Example sentiment labels (this should be based on your actual data)
data['sentiment'] = [1, 0, 1]  # Replace with your actual labels

# Encode the site names
site_encoder = LabelEncoder()
data['site_encoded'] = site_encoder.fit_transform(data['site'])

# Initialize the tokenizer (choose appropriate model)
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

# Tokenize the articles
encoded_articles = tokenizer(list(data['article']), padding=True, truncation=True, return_tensors='tf')

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    data[['site_encoded', 'article']],
    data['sentiment'],
    test_size=0.2,
    random_state=42
)

# Encode the training site names
site_train = X_train['site_encoded'].values  # This should be your training set site encodings
site_test = X_test['site_encoded'].values  # For testing

# Tokenize the articles for training and testing
encoded_train_articles = tokenizer(list(X_train['article']), padding=True, truncation=True, return_tensors='tf')
encoded_test_articles = tokenizer(list(X_test['article']), padding=True, truncation=True, return_tensors='tf')

# Now we can define the model as previously discussed

# Define the model structure
site_input = Input(shape=(1,), dtype='int32', name='site_input')
article_input_ids = Input(shape=(encoded_train_articles['input_ids'].shape[1],), dtype='int32', name='article_input_ids')
article_attention_mask = Input(shape=(encoded_train_articles['attention_mask'].shape[1],), dtype='int32', name='attention_mask')

# Site embedding
site_embedding = Embedding(input_dim=len(site_encoder.classes_), output_dim=10)(site_input)

# Article embedding using BERT
bert_model = TFBertModel.from_pretrained('bert-base-multilingual-cased')
article_embedding = bert_model(article_input_ids, attention_mask=article_attention_mask)[1]  # Pooler output

# Combine features
combined = concatenate([site_embedding, article_embedding])
x = Dense(64, activation='relu')(combined)
x = Dense(32, activation='relu')(x)
output = Dense(1, activation='sigmoid')(x)

# Build and compile the model
model = Model(inputs=[site_input, article_input_ids, article_attention_mask], outputs=output)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit([site_train, encoded_train_articles['input_ids'], encoded_train_articles['attention_mask']], y_train, epochs=5, batch_size=32)


# Prediction Function
def predict_positive_sentiment(website_name, entity_name):
    # Encode the website name
    website_encoded = site_encoder.transform([website_name])

    # Create a simplified input that directly relates the website to the entity
    sample_input = f"How does {website_name} view {entity_name}?"  # Template input
    sample_encoded = tokenizer(sample_input, padding=True, truncation=True, return_tensors='tf')

    # Make prediction
    prediction = model.predict([website_encoded, sample_encoded['input_ids'], sample_encoded['attention_mask']])
    probability = prediction[0][0] * 100  # Convert to percentage

    return f"Predicted Positive Tone Probability for {entity_name} on {website_name}: {probability:.2f}%"

# Example usage
print(predict_positive_sentiment('ESPN', 'Christian McCaffrey'))

