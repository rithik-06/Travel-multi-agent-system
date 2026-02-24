"""
Atlas - The Discovery Agent
Uses Llama 3.3 70B for destination discovery
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

# Configure LLM - Using Llama 3.3 70B
atlas_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Create Atlas Agent
atlas = Agent(
    role="Travel Discovery Specialist",
    goal="Find perfect travel destinations",
    backstory="""Expert traveler with 15 years experience. Find destinations matching 
    mood, interests, budget. Search once per destination. Be concise.""",
    tools=[web_search_tool],
    llm=atlas_llm,
    verbose=True,
    allow_delegation=False
)


if __name__ == "__main__":
    print("=" * 60)
    print("🗺️  ATLAS - Discovery Agent")
    print("=" * 60)
    print(f"Role: {atlas.role}")
    print(f"Model: llama-3.3-70b-versatile")
    print(f"Tools: {len(atlas.tools)}")
    print("=" * 60)