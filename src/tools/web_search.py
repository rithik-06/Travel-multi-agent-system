
#   Web search tool for agents to find travel information
##  Uses DuckDuckGo search (free, no API key needed)




from crewai.tools import BaseTool
from duckduckgo_search import DDGS


class WebSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = "Search the web for information about destinations, hotels, activities, etc. Input should be a search query."
    
    def _run(self, query: str) -> str:
        """
        Search the web
        
        Args:
            query: Search query (e.g., "best trekking destinations in Himalayas")
        
        Returns:
            Search results as formatted text
        """
        try:
            # Use DuckDuckGo search (free, no API needed)
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
            
            # Check if we got any results
            if not results:
                return f"No results found for: {query}"
            
            # Format results nicely for the agent
            formatted_results = f"Search results for '{query}':\n\n"
            
            for i, result in enumerate(results, 1):
                formatted_results += f"{i}. {result['title']}\n"
                formatted_results += f"   {result['body']}\n"
                formatted_results += f"   URL: {result['href']}\n\n"
            
            return formatted_results
            
        except Exception as e:
            return f"Search failed: {str(e)}"


# Create an instance of the tool
web_search_tool = WebSearchTool()


if __name__ == "__main__":
    # Test the tool
    print("Testing web search tool...\n")
    result = web_search_tool._run("best trekking spots in Himachal Pradesh")
    print(result)