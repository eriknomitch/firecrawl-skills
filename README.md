# Firecrawl Skills Test

[eriknomitch](https://erik.is)

**NOTE: This is just for a skills test, not an actual project.**

# NOTES/RESOURCES/SCRATCH

- https://context7.com/mendableai/firecrawl-docs

## Firecrawl Overview
From: https://docs.firecrawl.dev/introduction

### Features
- Scrape: scrapes a URL and get its content in LLM-ready format (markdown, structured data via LLM Extract, screenshot, html)
- Crawl: scrapes all the URLs of a web page and return content in LLM-ready format
- Map: input a website and get all the website urls - extremely fast
- Search: search the web and get full content from results
- Extract: get structured data from single page, multiple pages or entire websites with AI.

### Powerful Capabilities
- LLM-ready formats: markdown, structured data, screenshot, HTML, links, metadata
- The hard stuff: proxies, anti-bot mechanisms, dynamic content (js-rendered), output parsing, orchestration
- Customizability: exclude tags, crawl behind auth walls with custom headers, max crawl depth, etc…
- Media parsing: pdfs, docx, images.
- Reliability first: designed to get the data you need - no matter how hard it is.
- Actions: click, scroll, input, wait and more before extracting data

```
curl -X POST https://api.firecrawl.dev/v1/scrape \
    -H '
    Content-Type: application/json' \
    -H 'Authorization : Bearer YOUR_API_KEY' \
    -d '{
      "url": "https://docs.firecrawl.dev",
      "formats": ["markdown", "links", "html", "rawHtml", "screenshot"],
      "includeTags": ["h1", "p", "a", ".main-content"],
      "excludeTags": ["#ad", "#footer"],
      "onlyMainContent": false,
      "waitFor": 1000,
      "timeout": 15000
    }'
```
