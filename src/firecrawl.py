from ipdb import set_trace as st
from src.utility import get_firecrawl_api_key
from firecrawl import FirecrawlApp, JsonConfig, ScrapeOptions
import json
from typing import List
from dotenv import load_dotenv
from src.schemas import CompanyDetailsSchema
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

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
            print(f"{Fore.CYAN}Scraped content length:{Style.RESET_ALL} {len(markdown_content)} characters")
            print(markdown_content[:500])
        else:
            print(f"{Fore.RED}Markdown content not found in scrape_result.")
            print(f"{Fore.YELLOW}scrape_result:{Style.RESET_ALL}", scrape_result)


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

    print(f"{Fore.CYAN}Extracted data:{Style.RESET_ALL}")
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

        print(f"{Fore.CYAN}Crawled {len(data)} documents.{Style.RESET_ALL}")

        for doc in data:
            if hasattr(doc, "markdown"):
                print(f"{Fore.CYAN}Document URL:{Style.RESET_ALL} {doc.url}")
                print(f"{Fore.CYAN}Markdown content length:{Style.RESET_ALL} {len(doc.markdown)} characters")
                print(doc.markdown[:500])
                print(f"{Style.DIM}{'-' * 80}{Style.RESET_ALL}")


def run_example_search():
    # Perform a basic search
    search_result = app.search("firecrawl web scraping", limit=5)

    # Print the search results
    if search_result and hasattr(search_result, "data"):
        for result in search_result.data:
            print(f"{Fore.CYAN}Title:{Style.RESET_ALL} {result.get('title', 'N/A')}")
            print(f"{Fore.CYAN}URL:{Style.RESET_ALL} {result.get('url', 'N/A')}")
            print(f"{Fore.CYAN}Description:{Style.RESET_ALL} {result.get('description', 'N/A')}")
            print(f"{Style.DIM}{'-' * 40}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}No search results found or an error occurred.")
        print(f"{Fore.YELLOW}search_result:{Style.RESET_ALL}", search_result)


# =======================================================================
def run_examples():

    try:
        print(f"{Fore.YELLOW}{Style.BRIGHT}=== Basic Scraping ==={Style.RESET_ALL}")
        run_example_basic_scraping()

        print(f"\n{Fore.YELLOW}{Style.BRIGHT}=== Structured Extraction ==={Style.RESET_ALL}")
        run_example_structured_extraction()

        print(f"\n{Fore.YELLOW}{Style.BRIGHT}=== Crawling ==={Style.RESET_ALL}")
        run_example_crawl()

        print(f"\n{Fore.YELLOW}{Style.BRIGHT}=== Search Example ==={Style.RESET_ALL}")
        run_example_search()

    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}An error occurred: {str(e)}{Style.RESET_ALL}")
        st()

    print(f"{Fore.GREEN}{Style.BRIGHT}Examples completed successfully.{Style.RESET_ALL}")

    return
