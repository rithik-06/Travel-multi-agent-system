"""
Atlas - The Discovery Agent
Uses Mixtral model for destination discovery
"""

from crewai import Agent, LLM
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Setup paths
sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()

# Import tools
from tools.web_search import web_search_tool

# Configure LLM - Using Mixtral (separate rate limit!)
atlas_llm = LLM(
    model="groq/mixtral-8x7b-32768",
    api_key=os.getenv("GROQ_API_KEY")
)

# Create Atlas Agent
atlas = Agent(
    role="Travel Discovery Specialist",
    goal="Find perfect travel destinations matching user preferences and budget",
    backstory="""You are Atlas, an expert traveler with 15 years of global experience. 
    You find destinations that match travelers' moods, interests, and budgets. 
    You use web search efficiently - search once per destination. Be concise and specific.""",
    tools=[web_search_tool],
    llm=atlas_llm,
    verbose=True,
    allow_delegation=False
)


if __name__ == "__main__":
    print("=" * 60)
    print("🗺️  ATLAS - Discovery Agent (Mixtral)")
    print("=" * 60)
    print(f"Role: {atlas.role}")
    print(f"Model: mixtral-8x7b-32768")
    print(f"Tools: {len(atlas.tools)}")
    print("=" * 60)