"""
Shelter - The Accommodation Agent
Uses Llama 8B Instant for fast accommodation searches
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

# Configure LLM - Using Llama 8B (separate rate limit!)
shelter_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# Create Shelter Agent
shelter = Agent(
    role="Accommodation Specialist",
    goal="Find the best accommodations within budget and preferences",
    backstory="""You are Shelter, a hospitality expert with 12 years of experience. 
    You find value-for-money accommodations including hotels, homestays, and guesthouses. 
    You search efficiently and focus on location, price, and amenities. Be brief.""",
    tools=[web_search_tool],
    llm=shelter_llm,
    verbose=True,
    allow_delegation=False
)


if __name__ == "__main__":
    print("=" * 60)
    print("🏠 SHELTER - Accommodation Agent (Llama 8B)")
    print("=" * 60)
    print(f"Role: {shelter.role}")
    print(f"Model: llama-3.1-8b-instant")
    print(f"Tools: {len(shelter.tools)}")
    print("=" * 60)