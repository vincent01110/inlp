# import sys
# from pathlib import Path

# # Add sentiment-analyzer to sys.path
# sys.path.append(str(Path(__file__).parent.parent / "sentiment-analyzer"))

# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# import pandas as pd
# from pydantic import BaseModel
# from SentimentAnalyzer import SentimentAnalyzer

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all HTTP methods
#     allow_headers=["*"],  # Allows all headers
# )

# # Initialize the SentimentAnalyzer
# model = None

# def load_model():
#     global model
#     # Load the pretrained IMDB dataset model
#     imdb_dataset = pd.read_csv("hf://datasets/scikit-learn/imdb/IMDB Dataset.csv")
#     imdb_dataset = imdb_dataset.rename(columns={"review": "text"})
#     model = SentimentAnalyzer(imdb_dataset)

# load_model()

# # Define Pydantic model for the request body (except the file)
# class EntityRequest(BaseModel):
#     file_path: str  # Path to the CSV file
#     entity: str
#     site: str

# @app.get("/hello")
# def hello():
#     return JSONResponse('Hello')

# @app.post('/add')
# async def add_data():
#     return JSONResponse('Data added!', status_code=201)

# @app.post("/sentiment")
# async def get_entity_sentiment(request: EntityRequest):
#     """
#     Returns the average sentiment for a given entity mentioned on a specific site.
#     """
#     try:
#         # Read the CSV file with the correct delimiter (semicolon in this case)
#         news = pd.read_csv(request.file_path, delimiter=';')
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Error processing file: {e}")
    
#     # Check if necessary columns exist
#     print(news.columns)  # Print columns to debug
    
#     if 'text' not in news.columns:
#         raise HTTPException(status_code=400, detail="Missing 'text' column in the uploaded file")
#     if 'site' not in news.columns:
#         raise HTTPException(status_code=400, detail="Missing 'site' column in the uploaded file")

#     # Check if 'sentiment' column exists; if not, add it
#     if 'sentiment' not in news.columns:
#         # Initialize an empty list to store sentiment values
#         sentiments = []
#         for i in range(len(news)):
#             # Get the text for the current row
#             text = news.iloc[i]['text']  # Use iloc to safely access the text column
#             # Calculate the sentiment value using the model
#             sentiment = model.get_sentiment_value(text)
#             # Append the sentiment value to the list
#             sentiments.append(sentiment)
#         # Add the sentiments as a new column in the DataFrame
#         news['sentiment'] = sentiments

#     # Filter by site and entity
#     filtered_news = news[(news["site"].str.lower() == request.site.lower()) & (news["text"].str.contains(request.entity, case=False))]

#     if filtered_news.empty:
#         return JSONResponse(content={"entity": request.entity, "site": request.site, "sentiment": -1})

#     # Calculate the average sentiment
#     average_sentiment = float(filtered_news["sentiment"].mean())
#     return JSONResponse(content={"entity": request.entity, "site": request.site, "sentiment": average_sentiment})

# # Run the server with: uvicorn main:app --reload

import sys
from pathlib import Path

# Add sentiment-analyzer to sys.path
sys.path.append(str(Path(__file__).parent.parent / "sentiment-analyzer"))

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Text, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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

# Database setup
DATABASE_URL = "mysql+pymysql://root:mysql@localhost:3309/inlp"  # Update with your MySQL credentials
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the database schema
class Entry(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    site = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    sentiment = Column(Float, nullable=True)  # Nullable, populated later

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize the SentimentAnalyzer
model = None

def load_model():
    global model
    # Load the pretrained IMDB dataset model
    imdb_dataset = pd.read_csv("hf://datasets/scikit-learn/imdb/IMDB Dataset.csv")
    imdb_dataset = imdb_dataset.rename(columns={"review": "text"})
    model = SentimentAnalyzer(imdb_dataset)

load_model()

# Define Pydantic model for the request body
class EntityRequest(BaseModel):
    entity: str
    site: str

class AddRequest(BaseModel):
    site: str
    text: str

@app.get("/hello")
def hello():
    return JSONResponse('Hello')

@app.post('/add')
async def add_data(request: AddRequest):
    """
    Adds new data to the database.
    """
    db = SessionLocal()
    try:
        # Add data to the database
        new_entry = Entry(site=request.site, text=request.text)
        db.add(new_entry)
        db.commit()
        return JSONResponse(content={"message": "Data added!"}, status_code=201)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding data: {e}")
    finally:
        db.close()

@app.post("/sentiment")
async def get_entity_sentiment(request: EntityRequest):
    """
    Returns the average sentiment for a given entity mentioned on a specific site.
    """
    db = SessionLocal()
    try:
        # Query the database for the specified site and entity
        query = db.query(Entry).filter(
            Entry.site.ilike(request.site),
            Entry.text.ilike(f"%{request.entity}%")
        ).all()

        if not query:
            return JSONResponse(content={"entity": request.entity, "site": request.site, "sentiment": -1})

        # Calculate sentiment for entries without it
        sentiments = []
        for entry in query:
            if entry.sentiment is None:
                sentiment = model.get_sentiment_value(entry.text)
                entry.sentiment = float(sentiment)
                sentiments.append(float(sentiment))
                db.add(entry)  # Update the record
            else:
                sentiments.append(float(entry.sentiment))
        db.commit()

        # Calculate the average sentiment
        average_sentiment = sum(sentiments) / len(sentiments)
        return JSONResponse(content={"entity": request.entity, "site": request.site, "sentiment": average_sentiment})

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing sentiment: {e}")
    finally:
        db.close()

# Run the server with: uvicorn main:app --reload

