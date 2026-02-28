"""
Shelter - The Accommodation Agent
Uses Llama 3.1 8B for fast searches
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

# Configure LLM - Using Llama 3.1 8B
shelter_llm = LLM(
    model="huggingface/meta-llama/Meta-Llama-3-8B-Instruct",
    api_key=os.getenv("HUGGINGFACE_API_KEY")
)

# Create Shelter Agent
shelter = Agent(
    role="Accommodation Specialist",
    goal="Find best accommodations within budget",
    backstory="""Hospitality expert with 12 years experience. Find value accommodations. 
    Search efficiently. Focus on location, price, amenities. Be brief.""",
    tools=[web_search_tool],
    llm=shelter_llm,
    verbose=True,
    allow_delegation=False
)


if __name__ == "__main__":
    print("=" * 60)
    print("🏠 SHELTER - Accommodation Agent")
    print("=" * 60)
    print(f"Role: {shelter.role}")
    print(f"Model: llama-3.1-8b-instant")
    print(f"Tools: {len(shelter.tools)}")
    print("=" * 60)