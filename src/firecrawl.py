"""
Firecrawl Python Wrapper
A comprehensive wrapper for the Firecrawl API with organized methods for different scraping scenarios.
"""

from ipdb import set_trace as st
from src.utility import get_firecrawl_api_key
from firecrawl import FirecrawlApp, JsonConfig
import json
from typing import List  # Removed Dict, Optional, Union, Any

# Removed: import click, import time, from pathlib import Path, import pandas as pd
from pydantic import BaseModel, Field
from dotenv import load_dotenv

FIRECRAWL_API_KEY = get_firecrawl_api_key()

app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)


# ============================================================================
class NewsArticle(BaseModel):
    title: str = Field(description="The title of the news article")
    url: str = Field(description="The URL of the news article")
    author: str = Field(description="The author of the news article")
    date: str = Field(description="Publication date")
    summary: str = Field(description="Brief summary of the article")


class NewsSchema(BaseModel):
    articles: List[NewsArticle] = Field(description="List of news articles")


class Product(BaseModel):
    name: str = Field(description="Product name")
    price: float = Field(description="Product price")
    currency: str = Field(description="Currency code")
    description: str = Field(description="Product description")
    image_url: str = Field(description="Main product image URL")
    availability: str = Field(description="Product availability status")


# =======================================================================
def run_examples():

    try:
        # Example 1: Basic scraping
        print("=== Basic Scraping ===")
        # Directly use the global 'app' instance for scraping
        scrape_result = app.scrape_url(
            "https://news.ycombinator.com/newsguidelines.html", formats=["markdown"]
        )
        if scrape_result:
            # The FirecrawlApp.scrape_url returns a dictionary.
            # If 'markdown' is requested in formats, it should be a key in the result.
            markdown_content = scrape_result.get("markdown")
            if markdown_content:
                print(f"Scraped content length: {len(markdown_content)} characters")
                print(markdown_content[:500])
            else:
                print("Markdown content not found in scrape_result.")
                print("scrape_result:", scrape_result)

        # Example 2: Structured extraction
        print("\n=== Structured Extraction ===")
        # Construct JsonConfig for structured data extraction
        json_config = JsonConfig(
            extractionSchema=NewsSchema.model_json_schema(),
            mode="llm-extraction",
            pageOptions={"onlyMainContent": True},
            prompt="Extract the top stories with their details",
        )
        # Directly use the global 'app' instance for structured extraction
        scrape_result = app.scrape_url(
            "https://news.ycombinator.com",
            mode="llm-extract",
            json_options=json_config,
            formats=["json"],  # Requesting JSON output for structured data
        )

        if scrape_result:
            # The result for llm-extract with json format should contain a 'json' key
            # or directly be the extracted data. Based on Firecrawl docs, it's usually in 'llm_extraction' or 'data'.
            # The wrapper returned the whole response, which might have a specific key for this.
            # Let's assume the result structure from app.scrape_url for llm-extract is the data itself or under a specific key.
            # The original wrapper's extract_structured_data returned the direct result of app.scrape_url.
            # The Firecrawl SDK for scrape_url with mode='llm-extract' and json_options
            # returns a dict, and the extracted data is typically under the key 'llm_extraction'.
            # If 'formats=["json"]' is used, it might be under 'json'.
            # Let's print the result to see its structure before st()
            print("Structured extraction result:", scrape_result)
            st()

        # Example 3: Batch scraping
        # print("\n=== Batch Scraping ===")
        # urls = ["https://example.com", "https://httpbin.org/html"]
        # batch_data = wrapper.batch_scrape_sync(urls)
        # if batch_data:
        #     print(f"Scraped {len(batch_data.get('data', []))} URLs")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        st()

    return app
