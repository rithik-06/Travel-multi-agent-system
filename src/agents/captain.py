"""
Captain - The Orchestrator Agent
Coordinates Atlas, Shelter, and Buddy to create complete travel plans
"""

from crewai import Agent, LLM
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools (Captain doesn't use tools directly, but we import for reference)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


# Configure the LLM (brain) for Captain
captain_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Create Captain - The Orchestrator Agent
captain = Agent(
    role="Travel Planning Coordinator",
    goal="Create comprehensive, personalized travel plans by coordinating the discovery, accommodation, and community teams to deliver complete travel solutions",
    backstory="""You are Captain, an experienced travel planning coordinator with 
    20 years in the industry. You've orchestrated thousands of successful trips by 
    bringing together the right expertise at the right time. You understand that a 
    great trip needs three things: the perfect destination (Atlas finds this), 
    comfortable accommodation (Shelter finds this), and optionally great travel 
    companions (Buddy finds this). 
    
    You're a master at taking a traveler's vision and breaking it down into clear, 
    actionable tasks for your team. You know how to synthesize information from 
    multiple sources into one cohesive, exciting travel plan. You always start with 
    understanding the traveler's mood, budget, and preferences, then you coordinate 
    your team to deliver a complete solution.
    
    You're organized, detail-oriented, and excellent at communicating. You make sure 
    nothing falls through the cracks and that every recommendation makes sense 
    together as a complete package.""",
    tools=[],  # Captain doesn't use tools directly - delegates to other agents
    llm=captain_llm,
    verbose=True,
    allow_delegation=True  # This is KEY - Captain can delegate to other agents!
)


if __name__ == "__main__":
    # Test Captain
    print("=" * 60)
    print("👨‍✈️ CAPTAIN - Orchestrator Agent")
    print("=" * 60)
    print(f"Role: {captain.role}")
    print(f"Goal: {captain.goal}")
    print(f"Tools available: {len(captain.tools)}")
    print(f"Can delegate: {captain.allow_delegation}")
    print("=" * 60)