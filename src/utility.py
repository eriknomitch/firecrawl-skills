from dotenv import load_dotenv
import os

load_dotenv(".env.local", override=True)


def get_firecrawl_api_key():
    """Retrieve the Firecrawl API key from environment variables."""
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY environment variable is not set.")
    return api_key
