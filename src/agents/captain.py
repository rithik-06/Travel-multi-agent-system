"""
Captain - The Orchestrator Agent
Synthesizes all agent results without delegation
"""

from crewai import Agent, LLM
import os
from dotenv import load_dotenv

load_dotenv()

# Configure LLM
captain_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Create Captain Agent - NO DELEGATION
captain = Agent(
    role="Travel Planning Coordinator",
    goal="Synthesize team results into a complete travel plan",
    backstory="""You are a travel coordinator. You receive information from your team 
    (Atlas found destinations, Shelter found hotels, Buddy found groups) and you create 
    a final cohesive plan. 
    
    IMPORTANT: You do NOT search or delegate. You ONLY synthesize the information already 
    provided to you. Create a clear plan with: destination recommendation, top 3 accommodations, 
    budget breakdown, and 3-day itinerary. Maximum 500 words.""",
    tools=[],  # No tools
    llm=captain_llm,
    verbose=True,
    allow_delegation=False  # DISABLED!
)


if __name__ == "__main__":
    print("=" * 60)
    print("👨‍✈️ CAPTAIN - Orchestrator Agent")
    print("=" * 60)
    print(f"Role: {captain.role}")
    print(f"Model: llama-3.3-70b-versatile")
    print(f"Delegation: {captain.allow_delegation}")
    print("=" * 60)