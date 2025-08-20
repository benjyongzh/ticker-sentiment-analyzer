import os
from typing import List, Dict, Optional
import httpx

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
BASE_URL = "https://api.twitter.com/2"
MAX_TWEETS = int(os.getenv("MAX_TWEETS", "5"))


async def fetch_new_tweets(
    username: str, since_id: Optional[str] = None, limit: int = MAX_TWEETS
) -> List[Dict[str, str]]:
    if TWITTER_BEARER_TOKEN is None:
        raise RuntimeError("TWITTER_BEARER_TOKEN is not set")
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    async with httpx.AsyncClient() as client:
        user_resp = await client.get(
            f"{BASE_URL}/users/by/username/{username}", headers=headers
        )
        user_resp.raise_for_status()
        user_id = user_resp.json()["data"]["id"]
        params = {"max_results": min(limit, 100)}
        if since_id:
            params["since_id"] = since_id
        tweets_resp = await client.get(
            f"{BASE_URL}/users/{user_id}/tweets", headers=headers, params=params
        )
        tweets_resp.raise_for_status()
        return tweets_resp.json().get("data", [])[:limit]
