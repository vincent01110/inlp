import sys
from pathlib import Path

# Add sentiment-analyzer to sys.path
sys.path.append(str(Path(__file__).parent.parent / "sentiment-analyzer"))

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
from SentimentAnalyzer import SentimentAnalyzer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize the SentimentAnalyzer
model = None

def load_model():
    global model
    # Load the pretrained IMDB dataset model
    imdb_dataset = pd.read_csv("hf://datasets/scikit-learn/imdb/IMDB Dataset.csv")
    imdb_dataset = imdb_dataset.rename(columns={"review": "text"})
    model = SentimentAnalyzer(imdb_dataset)

load_model()

# Define Pydantic model for the request body (except the file)
class EntityRequest(BaseModel):
    file_path: str  # Path to the CSV file
    entity: str
    site: str

@app.get("/hello")
def hello():
    return JSONResponse('Hello')

@app.post("/get_entity_sentiment")
async def get_entity_sentiment(request: EntityRequest):
    """
    Returns the average sentiment for a given entity mentioned on a specific site.
    """
    try:
        # Read the CSV file with the correct delimiter (semicolon in this case)
        news = pd.read_csv(request.file_path, delimiter=';')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {e}")
    
    # Check if necessary columns exist
    print(news.columns)  # Print columns to debug
    
    if 'text' not in news.columns:
        raise HTTPException(status_code=400, detail="Missing 'text' column in the uploaded file")
    if 'site' not in news.columns:
        raise HTTPException(status_code=400, detail="Missing 'site' column in the uploaded file")

    # Check if 'sentiment' column exists; if not, add it
    if 'sentiment' not in news.columns:
        # Initialize an empty list to store sentiment values
        sentiments = []
        for i in range(len(news)):
            # Get the text for the current row
            text = news.iloc[i]['text']  # Use iloc to safely access the text column
            # Calculate the sentiment value using the model
            sentiment = model.get_sentiment_value(text)
            # Append the sentiment value to the list
            sentiments.append(sentiment)
        # Add the sentiments as a new column in the DataFrame
        news['sentiment'] = sentiments

    # Filter by site and entity
    filtered_news = news[(news["site"] == request.site) & (news["text"].str.contains(request.entity, case=False))]

    if filtered_news.empty:
        return JSONResponse(content={"entity": request.entity, "site": request.site, "sentiment": -1})

    # Calculate the average sentiment
    average_sentiment = float(filtered_news["sentiment"].mean())
    return JSONResponse(content={"entity": request.entity, "site": request.site, "sentiment": average_sentiment})

# Run the server with: uvicorn main:app --reload
