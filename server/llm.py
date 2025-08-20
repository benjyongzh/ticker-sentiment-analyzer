import os
import json
from typing import List

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

async def analyze_tweets(texts: List[str]):
    """Analyze many tweets in a single LLM call.

    The model receives a list of tweets and is responsible for
    identifying any publicly traded companies mentioned in each. It
    returns JSON objects of the form {"tweet_index": int, "ticker":
    str, "sentiment": str} for every company referenced. The model may
    need to infer ticker symbols when only the company name is
    provided.
    """
    if openai.api_key is None or not texts:
        return []

    tweet_lines = [f"{i}. {text}" for i, text in enumerate(texts)]

    prompt = (
        "For each tweet below, identify any publicly traded companies "
        "referenced and return their stock ticker symbol and the sentiment "
        "expressed about each. Respond with a JSON array of objects with "
        "'tweet_index', 'ticker', and 'sentiment' keys.\n\nTweets:\n"
        + "\n".join(tweet_lines)
    )

    resp = await openai.ChatCompletion.acreate(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You assess stock sentiment."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    content = resp["choices"][0]["message"]["content"]
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            data = [data]
        return data
    except Exception:
        return []


# Backwards compatibility with previous single-tweet usage
async def analyze_tweet(text: str):
    results = await analyze_tweets([text])
    if not results:
        return []
    # Filter results for tweet_index 0 and drop the index field
    out = []
    for r in results:
        if r.get("tweet_index") == 0:
            out.append({k: v for k, v in r.items() if k != "tweet_index"})
    return out
