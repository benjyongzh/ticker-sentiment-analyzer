from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import ValidationError

from . import models, schemas, twitter_client, llm
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/analyze", response_model=schemas.AnalyzeResponse)
async def analyze(request: schemas.AnalyzeRequest, db: Session = Depends(get_db)):
    account = db.query(models.TwitterAccount).filter_by(username=request.username).first()
    if account is None:
        account = models.TwitterAccount(username=request.username)
        db.add(account)
        db.commit()
        db.refresh(account)

    tweets = await twitter_client.fetch_new_tweets(request.username, account.last_tweet_id)
    sentiments_out: List[schemas.TickerSentimentSchema] = []
    max_id = account.last_tweet_id
    for tweet in tweets:
        tweet_obj = models.Tweet(id=tweet["id"], account_id=account.id, content=tweet["text"])
        db.add(tweet_obj)
        sentiments = await llm.analyze_tweet(tweet["text"])
        for s in sentiments:
            try:
                ts_schema = schemas.TickerSentimentSchema(**s)
            except ValidationError:
                continue
            ts = models.TickerSentiment(
                ticker=ts_schema.ticker,
                sentiment=ts_schema.sentiment,
                account_id=account.id,
                tweet_id=tweet["id"],
            )
            db.add(ts)
            sentiments_out.append(ts_schema)
        if max_id is None or tweet["id"] > max_id:
            max_id = tweet["id"]
    if max_id:
        account.last_tweet_id = max_id
    db.commit()
    return schemas.AnalyzeResponse(new_tweets=len(tweets), sentiments=sentiments_out)
