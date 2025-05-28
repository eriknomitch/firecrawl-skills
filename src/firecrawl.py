from ipdb import set_trace as st
from src.utils import get_api_key
from firecrawl import FirecrawlApp
import click

FIRECRAWL_API_KEY = get_firecrawl_api_key()

@app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# Scrape a website:
scrape_result = app.scrape_url("firecrawl.dev", formats=["markdown", "html"])
print(scrape_result)
