import enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from .database import Base


class Sentiment(str, enum.Enum):
    bullish = "bullish"
    bearish = "bearish"
    neutral = "neutral"


class TwitterAccount(Base):
    __tablename__ = "twitter_accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    last_tweet_id = Column(String, nullable=True)

    tweets = relationship("Tweet", back_populates="account")


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(String, primary_key=True)
    account_id = Column(Integer, ForeignKey("twitter_accounts.id"), nullable=False)
    content = Column(Text, nullable=False)

    account = relationship("TwitterAccount", back_populates="tweets")
    sentiments = relationship("TickerSentiment", back_populates="tweet")


class TickerSentiment(Base):
    __tablename__ = "ticker_sentiments"

    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    sentiment = Column(SqlEnum(Sentiment, name="sentiment_enum"), nullable=False)
    account_id = Column(Integer, ForeignKey("twitter_accounts.id"), nullable=False)
    tweet_id = Column(String, ForeignKey("tweets.id"), nullable=False)

    account = relationship("TwitterAccount")
    tweet = relationship("Tweet", back_populates="sentiments")
