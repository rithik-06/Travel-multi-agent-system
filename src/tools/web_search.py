"""
Web search tool - uses DuckDuckGo (free, no API key needed)
"""

from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web for travel information.
    Returns formatted results as a string that agents can reason over.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return f"No results found for: {query}"

        formatted = f"Search results for '{query}':\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result['title']}\n"
            formatted += f"   {result['body'][:300]}\n"
            formatted += f"   URL: {result['href']}\n\n"

        return formatted

    except Exception as e:
        return f"Search failed: {str(e)}"


if __name__ == "__main__":
    result = web_search("best trekking spots in Himachal Pradesh")
    print(result)