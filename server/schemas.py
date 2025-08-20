from pydantic import BaseModel
from typing import List
from .models import Sentiment


class AnalyzeRequest(BaseModel):
    username: str


class TickerSentimentSchema(BaseModel):
    ticker: str
    sentiment: Sentiment


class AnalyzeResponse(BaseModel):
    new_tweets: int
    sentiments: List[TickerSentimentSchema]
