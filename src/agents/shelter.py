"""
Shelter - The Accommodation Agent
Finds perfect hotels, homestays, and accommodations based on budget and preferences
"""

from crewai import Agent, LLM
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.web_search import web_search_tool


# Configure the LLM (brain) for Shelter
shelter_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# Create Shelter - The Accommodation Agent

shelter = Agent(
    role="Accommodation Specialist",
    goal="Find the best hotels, homestays, and accommodations that match the traveler's budget, preferences, and destination",
    backstory="""You are Shelter, an expert accommodation finder with 12 years of 
    experience in the hospitality industry. You have connections with hotels, homestays, 
    guesthouses, and unique lodging options around the world. You're brilliant at finding 
    hidden gem accommodations that offer great value for money. You understand that the 
    right place to stay can make or break a trip, so you always consider factors like 
    location, cleanliness, amenities, host quality, and authentic local experiences. 
    You're passionate about helping travelers find their perfect "home away from home".
    
    IMPORTANT: You can ONLY use the 'Web Search' tool to find accommodations. 
    When searching, use queries like: 'budget hotels in [destination]', 
    'homestays near [location]', 'guesthouses [city] under $30'.
    Do NOT try to use any other tools.""",
    tools=[web_search_tool],
    llm=shelter_llm,
    verbose=True,
    allow_delegation=False
)

if __name__ == "__main__":
    # Test Shelter
    print("=" * 60)
    print("🏠 SHELTER - Accommodation Agent")
    print("=" * 60)
    print(f"Role: {shelter.role}")
    print(f"Goal: {shelter.goal}")
    print(f"Tools available: {len(shelter.tools)}")
    print("=" * 60)