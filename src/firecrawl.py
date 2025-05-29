"""
Firecrawl Python Wrapper
A comprehensive wrapper for the Firecrawl API with organized methods for different scraping scenarios.
"""

from ipdb import set_trace as st
from src.utility import get_firecrawl_api_key
from firecrawl import FirecrawlApp, JsonConfig, ScrapeOptions
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
    class ExtractSchema(BaseModel):
        company_mission: str
        supports_sso: bool
        is_open_source: bool
        is_in_yc: bool

    data = app.extract(
        [
            "https://docs.firecrawl.dev/*",
            "https://firecrawl.dev/",
            "https://www.ycombinator.com/companies/",
        ],
        prompt="Extract the company mission, whether it supports SSO, whether it is open source, and whether it is in Y Combinator from the page.",
        schema=ExtractSchema.model_json_schema(),
    )

    print(data)


def run_example_crawl():
    crawl_status = app.crawl_url(
        "https://firecrawl.dev",
        limit=100,
        scrape_options=ScrapeOptions(formats=["markdown", "html"]),
        poll_interval=30,
    )

    print(crawl_status)


# =======================================================================
def run_examples():

    try:
        print("=== Basic Scraping ===")
        run_example_basic_scraping()

        print("\n=== Structured Extraction ===")
        run_example_structured_extraction()

        print("\n=== Crawling ===")
        run_example_crawl()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        st()

    print("Examples completed successfully.")

    return
