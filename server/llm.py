import os
import json
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


async def analyze_tweet(text: str):
    if openai.api_key is None:
        return []
    prompt = (
        "Extract stock ticker symbols mentioned in the tweet and classify each as bullish, bearish, or neutral. "
        "Return a JSON array of objects with 'ticker' and 'sentiment' keys.\n"
        f"Tweet: {text}"
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
            return [data]
        return data
    except Exception:
        return []
