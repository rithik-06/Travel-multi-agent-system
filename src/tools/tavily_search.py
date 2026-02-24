"""
Tavily Search Tool - Better web search
"""

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()


class TavilySearchInput(BaseModel):
    """Input for Tavily search"""
    query: str = Field(..., description="Search query")


class TavilySearchTool(BaseTool):
    name: str = "tavily_search"
    description: str = "Search the web for travel information. Use this to find destinations, hotels, and travel tips."
    args_schema: Type[BaseModel] = TavilySearchInput
    
    def _run(self, query: str) -> str:
        """Execute Tavily search"""
        try:
            from tavily import TavilyClient
            
            api_key = os.getenv("TAVILY_API_KEY")
            if not api_key:
                return "Tavily API key not configured"
            
            client = TavilyClient(api_key=api_key)
            
            # Search
            response = client.search(
                query=query,
                max_results=5
            )
            
            if not response or 'results' not in response:
                return f"No results for: {query}"
            
            # Format results
            output = f"Search results for '{query}':\n\n"
            
            for i, result in enumerate(response['results'], 1):
                output += f"{i}. {result['title']}\n"
                output += f"   {result['content'][:150]}...\n"
                output += f"   Source: {result['url']}\n\n"
            
            return output
            
        except Exception as e:
            return f"Search error: {str(e)}"


# Create instance
tavily_search_tool = TavilySearchTool()


if __name__ == "__main__":
    print("Testing Tavily...")
    result = tavily_search_tool._run("best trekking in Himalayas")
    print(result)