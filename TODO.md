# TODO
- [ ] Update the README with the latest features and usage instructions.
- [x] Change the name of ExtractSchema to be more specific to its functionality.
- [x] Add an example test run for Search. Example python:

```
from firecrawl import FirecrawlApp

# Initialize the client with your API key
app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Perform a basic search
search_result = app.search("firecrawl web scraping", limit=5)

# Print the search results
for result in search_result.data:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Description: {result['description']}")
```
