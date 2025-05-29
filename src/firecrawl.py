from ipdb import set_trace as st
from src.utility import get_firecrawl_api_key
from firecrawl import FirecrawlApp, JsonConfig, ScrapeOptions
import json
from typing import List
from dotenv import load_dotenv
from src.schemas import CompanyDetailsSchema

FIRECRAWL_API_KEY = get_firecrawl_api_key()

app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)


# =======================================================================
def run_example_basic_scraping():
    scrape_result = app.scrape_url(
        "https://news.ycombinator.com/newsguidelines.html",
        formats=["markdown", "html"],
    )
    if scrape_result:
        markdown_content = (
            scrape_result.markdown if hasattr(scrape_result, "markdown") else None
        )
        if markdown_content:
            print(f"Scraped content length: {len(markdown_content)} characters")
            print(markdown_content[:500])
        else:
            print("Markdown content not found in scrape_result.")
            print("scrape_result:", scrape_result)


def run_example_structured_extraction():
    data = app.extract(
        [
            "https://docs.firecrawl.dev/*",
            "https://firecrawl.dev/",
            "https://www.ycombinator.com/companies/",
        ],
        prompt="Extract the company mission, whether it supports SSO, whether it is open source, and whether it is in Y Combinator from the page.",
        schema=CompanyDetailsSchema.model_json_schema(),
    )

    print(data)


def run_example_crawl():
    crawl_result = app.crawl_url(
        "https://firecrawl.dev",
        limit=10,
        scrape_options=ScrapeOptions(formats=["markdown", "html"]),
        poll_interval=30,
    )

    if crawl_result:
        # List of FirecrawlDocument objects
        data = crawl_result.data

        print(f"Crawled {len(data)} documents.")

        for doc in data:
            if hasattr(doc, "markdown"):
                print(f"Document URL: {doc.url}")
                print(f"Markdown content length: {len(doc.markdown)} characters")
                print(doc.markdown[:500])
                print("-" * 80)


def run_example_search():
    # Perform a basic search
    search_result = app.search("firecrawl web scraping", limit=5)

    # Print the search results
    if search_result and hasattr(search_result, "data"):
        for result in search_result.data:
            print(f"Title: {result.get('title', 'N/A')}")
            print(f"URL: {result.get('url', 'N/A')}")
            print(f"Description: {result.get('description', 'N/A')}")
            print("-" * 40)
    else:
        print("No search results found or an error occurred.")
        print("search_result:", search_result)


# =======================================================================
def run_examples():

    try:
        print("=== Basic Scraping ===")
        run_example_basic_scraping()

        print("\n=== Structured Extraction ===")
        run_example_structured_extraction()

        print("\n=== Crawling ===")
        run_example_crawl()

        print("\n=== Search Example ===")
        run_example_search()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        st()

    print("Examples completed successfully.")

    return
