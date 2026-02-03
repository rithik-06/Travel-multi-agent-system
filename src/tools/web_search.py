
#   Web search tool for agents to find travel information
##  Uses DuckDuckGo search (free, no API key needed)


from json import tool
from json import tool
from crewai.tools import BaseTool
from pydantic import Field
from duckduckgo_search import DDGS
from monitoring import log_api_call, setup_logger 

logger = setup_logger("web_search")


@tool("Web Search")
def web_search_tool(query: str) -> str:
    """
    Search the web for information about destinations, hotels, activities, etc.
    
    Args:
        query: Search query (e.g., "best trekking destinations in Himalayas")
    
    Returns:
        Search results as formatted text
    """
    try:
        logger.info(f"Searching web for: {query}")
        
        # Use DuckDuckGo search (free, no API needed)
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        
        # Format results
        if not results:
            return f"No results found for: {query}"
        
        formatted_results = f"Search results for '{query}':\n\n"
        for i, result in enumerate(results, 1):
            formatted_results += f"{i}. {result['title']}\n"
            formatted_results += f"   {result['body']}\n"
            formatted_results += f"   URL: {result['href']}\n\n"
        
        # Log the API call
        log_api_call("DuckDuckGo", "search", tokens_used=None, cost=0.0)
        
        logger.info(f"Found {len(results)} results")
        return formatted_results
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return f"Search failed: {str(e)}"


if __name__ == "__main__":
    # Test the tool
    print("Testing web search tool...\n")
    result = web_search_tool("best trekking spots in Himachal Pradesh")
    print(result)