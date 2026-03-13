"""
Atlas - Discovery Agent
Uses OpenRouter (Free Llama 3 model)
"""

from crewai import Agent, LLM
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Setup
sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()

# Import tools
try:
    from tools.tavily_search import tavily_search_tool
    TOOL = tavily_search_tool
except:
    from tools.web_search import web_search_tool
    TOOL = web_search_tool

# OpenRouter LLM
atlas_llm = LLM(
    model="openrouter/meta-llama/llama-3-8b-instruct:free",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Create Atlas
atlas = Agent(
    role="Travel Discovery Specialist",
    goal="Find 3 perfect destinations matching user preferences",
    backstory="Expert traveler. Find destinations efficiently. Search once per destination.",
    tools=[TOOL],
    llm=atlas_llm,
    verbose=True,
    allow_delegation=False
)


if __name__ == "__main__":
    print("=" * 60)
    print("🗺️  ATLAS - Discovery Agent")
    print("=" * 60)
    print(f"Provider: OpenRouter")
    print(f"Model: Llama 3 8B (Free)")
    print(f"Tools: {len(atlas.tools)}")
    print("=" * 60)