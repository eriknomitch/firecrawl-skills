"""
Firecrawl Python Wrapper
A comprehensive wrapper for the Firecrawl API with organized methods for different scraping scenarios.
"""

from ipdb import set_trace as st
from src.utility import get_firecrawl_api_key
from firecrawl import FirecrawlApp, JsonConfig
import click
import json
import time
from typing import Dict, List, Optional, Union, Any
from pathlib import Path
import pandas as pd
from pydantic import BaseModel, Field
from dotenv import load_dotenv

FIRECRAWL_API_KEY = get_firecrawl_api_key()

app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)


class FirecrawlWrapper:
    """
    A comprehensive wrapper for Firecrawl API with organized scraping methods.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Firecrawl wrapper.

        Args:
            api_key: Optional API key. If not provided, will use FIRECRAWL_API_KEY from environment.
        """
        self.app = (
            FirecrawlApp(api_key=FIRECRAWL_API_KEY) if api_key else FirecrawlApp()
        )

    # ============================================================================
    # BASIC SCRAPING METHODS
    # ============================================================================

    def scrape_basic(self, url: str, formats: List[str] = None) -> Dict[str, Any]:
        if formats is None:
            formats = ["markdown"]

        try:
            return self.app.scrape_url(url, formats=formats)
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None

    def scrape_multiple_formats(
        self,
        url: str,
        formats: List[str] = None,
        include_screenshot: bool = False,
        full_page_screenshot: bool = False,
    ) -> Dict[str, Any]:
        """
        Scrape a URL with multiple output formats.

        Args:
            url: The URL to scrape
            formats: List of desired formats (html, rawHtml, markdown, links)
            include_screenshot: Whether to include a viewport screenshot
            full_page_screenshot: Whether to include a full-page screenshot

        Returns:
            Dictionary containing all requested formats

        Example:
            >>> data = wrapper.scrape_multiple_formats(
            ...     'https://example.com',
            ...     formats=['html', 'markdown', 'links'],
            ...     include_screenshot=True
            ... )
        """
        if formats is None:
            formats = ["markdown", "html"]

        if include_screenshot:
            formats.append("screenshot")
        if full_page_screenshot:
            formats.append("screenshot@fullPage")

        return self.scrape_basic(url, formats)

    def scrape_with_filters(
        self,
        url: str,
        include_tags: List[str] = None,
        exclude_tags: List[str] = None,
        only_main_content: bool = False,
    ) -> Dict[str, Any]:
        """
        Scrape a URL with content filtering options.

        Args:
            url: The URL to scrape
            include_tags: HTML tags to specifically include
            exclude_tags: HTML tags to exclude
            only_main_content: Whether to extract only main content

        Returns:
            Dictionary containing filtered scraped data

        Example:
            >>> data = wrapper.scrape_with_filters(
            ...     'https://example.com',
            ...     include_tags=['p', 'h1', 'h2'],
            ...     exclude_tags=['nav', 'footer'],
            ...     only_main_content=True
            ... )
        """
        params = {}

        if include_tags:
            params["includeTags"] = include_tags
        if exclude_tags:
            params["excludeTags"] = exclude_tags
        if only_main_content:
            params["onlyMainContent"] = True

        try:
            return self.app.scrape_url(url, params=params)
        except Exception as e:
            print(f"Error scraping {url} with filters: {str(e)}")
            return None

    def scrape_pdf(self, pdf_url: str) -> Dict[str, Any]:
        """
        Scrape content from a PDF file.

        Args:
            pdf_url: URL pointing to a PDF file

        Returns:
            Dictionary containing PDF content converted to markdown

        Example:
            >>> data = wrapper.scrape_pdf('https://example.com/document.pdf')
            >>> print(data['markdown'])
        """
        try:
            return self.app.scrape_url(pdf_url)
        except Exception as e:
            print(f"Error scraping PDF {pdf_url}: {str(e)}")
            return None

    # ============================================================================
    # EXTRACTION METHODS
    # ============================================================================

    def extract_with_prompt(
        self,
        url: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        include_screenshot: bool = False,
    ) -> Dict[str, Any]:
        """
        Extract specific data using natural language prompts.

        Args:
            url: The URL to scrape
            prompt: Natural language prompt describing what to extract
            system_prompt: Optional system prompt to guide the LLM
            include_screenshot: Whether to include a screenshot

        Returns:
            Dictionary containing extracted data

        Example:
            >>> data = wrapper.extract_with_prompt(
            ...     'https://news.ycombinator.com',
            ...     "Extract the top 5 story titles and their URLs"
            ... )
            >>> print(data['extract'])
        """
        formats = ["markdown", "extract"]
        if include_screenshot:
            formats.append("screenshot")

        params = {"formats": formats, "extract": {"prompt": prompt}}

        if system_prompt:
            params["extract"]["systemPrompt"] = system_prompt

        try:
            return self.app.scrape_url(url, params=params)
        except Exception as e:
            print(f"Error extracting from {url}: {str(e)}")
            return None

    def extract_structured_data(
        self,
        url: str,
        schema: Union[Dict, BaseModel],
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        try:
            json_config = JsonConfig(
                extractionSchema=schema.model_json_schema(),
                mode="llm-extraction",
                pageOptions={"onlyMainContent": True},
                prompt=prompt,
                systemPrompt=system_prompt,
            )

            return self.app.scrape_url(
                url,
                formats=["json"],
                mode="llm-extract",
                json_options=json_config,
            )
        except Exception as e:
            print(f"Error extracting structured data from {url}: {str(e)}")
            return None

    # ============================================================================
    # INTERACTIVE SCRAPING METHODS
    # ============================================================================

    def scrape_with_actions(
        self,
        url: str,
        actions: List[Dict[str, Any]],
        extraction_params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Scrape a page after performing interactive actions.

        Args:
            url: The URL to scrape
            actions: List of actions to perform (click, type, wait, etc.)
            extraction_params: Optional extraction parameters

        Returns:
            Dictionary containing scraped data after actions

        Example:
            >>> actions = [
            ...     {"type": "wait", "milliseconds": 2000},
            ...     {"type": "click", "selector": "#search-button"},
            ...     {"type": "write", "text": "search term"},
            ...     {"type": "wait", "milliseconds": 1000}
            ... ]
            >>> data = wrapper.scrape_with_actions('https://example.com', actions)
        """
        params = {"formats": ["markdown"], "actions": actions}

        if extraction_params:
            params["formats"].append("extract")
            params["extract"] = extraction_params

        try:
            return self.app.scrape_url(url, params=params)
        except Exception as e:
            print(f"Error scraping {url} with actions: {str(e)}")
            return None

    def scrape_dynamic_content(
        self,
        url: str,
        wait_for_selector: str = None,
        wait_time: int = 3000,
        click_elements: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Scrape dynamic content that requires waiting or clicking.

        Args:
            url: The URL to scrape
            wait_for_selector: CSS selector to wait for
            wait_time: Time to wait in milliseconds
            click_elements: List of CSS selectors to click

        Returns:
            Dictionary containing scraped dynamic content

        Example:
            >>> data = wrapper.scrape_dynamic_content(
            ...     'https://spa-app.com',
            ...     wait_for_selector='.content-loaded',
            ...     click_elements=['#show-more-button']
            ... )
        """
        actions = [{"type": "wait", "milliseconds": wait_time}]

        if click_elements:
            for selector in click_elements:
                actions.append({"type": "click", "selector": selector})
                actions.append({"type": "wait", "milliseconds": 1000})

        if wait_for_selector:
            actions.append({"type": "wait", "selector": wait_for_selector})

        return self.scrape_with_actions(url, actions)

    # ============================================================================
    # BATCH SCRAPING METHODS
    # ============================================================================

    def batch_scrape_sync(
        self,
        urls: List[str],
        formats: List[str] = None,
        extraction_params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Scrape multiple URLs synchronously in a batch.

        Args:
            urls: List of URLs to scrape
            formats: Desired output formats
            extraction_params: Optional extraction parameters

        Returns:
            Dictionary containing batch scraping results

        Example:
            >>> urls = ['https://site1.com', 'https://site2.com']
            >>> data = wrapper.batch_scrape_sync(urls, formats=['markdown'])
            >>> for item in data['data']:
            ...     print(item['markdown'])
        """
        if formats is None:
            formats = ["markdown"]

        params = {"formats": formats}

        if extraction_params:
            params["extract"] = extraction_params
            if "extract" not in formats:
                params["formats"].append("extract")

        try:
            return self.app.batch_scrape_urls(urls, params=params)
        except Exception as e:
            print(f"Error in batch scraping: {str(e)}")
            return None

    def batch_scrape_async(
        self,
        urls: List[str],
        formats: List[str] = None,
        extraction_params: Optional[Dict] = None,
    ) -> Dict[str, str]:
        """
        Submit a batch scraping job to run asynchronously.

        Args:
            urls: List of URLs to scrape
            formats: Desired output formats
            extraction_params: Optional extraction parameters

        Returns:
            Dictionary containing job ID and status URL

        Example:
            >>> job = wrapper.batch_scrape_async(urls)
            >>> status = wrapper.check_batch_status(job['id'])
        """
        if formats is None:
            formats = ["markdown"]

        params = {"formats": formats}

        if extraction_params:
            params["extract"] = extraction_params
            if "extract" not in formats:
                params["formats"].append("extract")

        try:
            return self.app.async_batch_scrape_urls(urls, params=params)
        except Exception as e:
            print(f"Error submitting batch job: {str(e)}")
            return None

    def check_batch_status(self, job_id: str) -> Dict[str, Any]:
        """
        Check the status of an asynchronous batch scraping job.

        Args:
            job_id: The job ID returned from batch_scrape_async

        Returns:
            Dictionary containing job status and results

        Example:
            >>> status = wrapper.check_batch_status('job-123')
            >>> print(f"Progress: {status['completed']}/{status['total']}")
        """
        try:
            return self.app.check_batch_scrape_status(job_id)
        except Exception as e:
            print(f"Error checking batch status: {str(e)}")
            return None

    def wait_for_batch_completion(
        self, job_id: str, poll_interval: int = 30, max_wait_time: int = 3600
    ) -> Dict[str, Any]:
        """
        Wait for a batch job to complete and return results.

        Args:
            job_id: The job ID to wait for
            poll_interval: Seconds between status checks
            max_wait_time: Maximum time to wait in seconds

        Returns:
            Dictionary containing completed job results
        """
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            status = self.check_batch_status(job_id)

            if not status:
                return None

            if status.get("status") == "completed":
                return status
            elif status.get("status") == "failed":
                print(f"Batch job {job_id} failed")
                return status

            print(
                f"Job {job_id}: {status.get('completed', 0)}/{status.get('total', 0)} completed"
            )
            time.sleep(poll_interval)

        print(f"Batch job {job_id} timed out after {max_wait_time} seconds")
        return self.check_batch_status(job_id)

    # ============================================================================
    # CRAWLING METHODS
    # ============================================================================

    def crawl_website(
        self,
        url: str,
        limit: int = 100,
        max_depth: int = None,
        formats: List[str] = None,
        include_subdomains: bool = False,
        exclude_paths: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Crawl an entire website and scrape multiple pages.

        Args:
            url: The starting URL to crawl
            limit: Maximum number of pages to crawl
            max_depth: Maximum crawl depth
            formats: Desired output formats for each page
            include_subdomains: Whether to include subdomains
            exclude_paths: URL paths to exclude from crawling

        Returns:
            Dictionary containing crawl results

        Example:
            >>> results = wrapper.crawl_website(
            ...     'https://blog.example.com',
            ...     limit=50,
            ...     max_depth=2,
            ...     formats=['markdown']
            ... )
        """
        if formats is None:
            formats = ["markdown"]

        scrape_options = {"formats": formats}

        crawl_params = {"limit": limit, "scrape_options": scrape_options}

        if max_depth is not None:
            crawl_params["maxDepth"] = max_depth
        if not include_subdomains:
            crawl_params["allowExternalLinks"] = False
        if exclude_paths:
            crawl_params["excludePaths"] = exclude_paths

        try:
            return self.app.crawl_url(url, **crawl_params)
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
            return None

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def save_to_json(
        self, data: Dict[str, Any], filepath: Union[str, Path], indent: int = 2
    ) -> bool:
        """
        Save scraped data to a JSON file.

        Args:
            data: The data to save
            filepath: Path to save the file
            indent: JSON indentation

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving to JSON: {str(e)}")
            return False

    def save_to_csv(self, data: List[Dict], filepath: Union[str, Path]) -> bool:
        """
        Save list of dictionaries to CSV file.

        Args:
            data: List of dictionaries to save
            filepath: Path to save the file

        Returns:
            True if successful, False otherwise
        """
        try:
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
            return True
        except Exception as e:
            print(f"Error saving to CSV: {str(e)}")
            return False

    def extract_links(self, data: Dict[str, Any]) -> List[str]:
        """
        Extract all links from scraped data.

        Args:
            data: Scraped data containing links

        Returns:
            List of URLs found in the data
        """
        return data.get("links", [])

    def get_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract metadata from scraped data.

        Args:
            data: Scraped data

        Returns:
            Metadata dictionary
        """
        return data.get("metadata", {})

    def convert_to_dataframe(self, data_list: List[Dict]) -> pd.DataFrame:
        """
        Convert list of scraped data dictionaries to pandas DataFrame.

        Args:
            data_list: List of data dictionaries

        Returns:
            Pandas DataFrame
        """
        return pd.DataFrame(data_list)


# ============================================================================
# EXAMPLE USAGE AND HELPER FUNCTIONS
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
# MAIN EXECUTION BLOCK
# =======================================================================


def run_examples():

    try:
        # Initialize wrapper
        wrapper = FirecrawlWrapper()

        # Example 1: Basic scraping
        print("=== Basic Scraping ===")
        scrape_result = wrapper.scrape_basic(
            "https://news.ycombinator.com/newsguidelines.html", formats=["markdown"]
        )
        if scrape_result:
            markdown_content = scrape_result.markdown

            print(f"Scraped content length: {len(markdown_content)} characters")

            print(markdown_content[:500])

        # Example 2: Structured extraction
        print("\n=== Structured Extraction ===")
        scrape_result = wrapper.extract_structured_data(
            "https://news.ycombinator.com",
            schema=NewsSchema,
            prompt="Extract the top stories with their details",
        )

        if scrape_result:
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

    return wrapper
