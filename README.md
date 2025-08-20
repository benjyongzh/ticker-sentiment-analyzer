# ticker-sentiment-analyzer

FastAPI service that evaluates ticker sentiment from Twitter accounts.

## Development

1. Copy `.env.example` to `.env` and fill in your API keys. Available settings:
   - `TWITTER_BEARER_TOKEN`
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL` (defaults to `gpt-3.5-turbo`)
   - `DATABASE_URL`
   - `MAX_TWEETS` (maximum tweets analyzed per request, defaults to 5)
2. Run the API using [uv](https://github.com/astral-sh/uv):

```bash
uv run uvicorn server.main:app --reload
```
