##  Atlas - The Discovery Agent
### Finds perfect travel destinations based on user mood and preferences

from crewai import Agent
from crewai import LLM
import os
from dotenv import load_dotenv

## load environment variables from .env file
load_dotenv()

## import the custom tools
import sys 
from pathlib import Path   
sys.path.insert(0, str(Path(__file__).parent.parent ))

from tools.web_search import web_search_tool


# Configure the LLM (brain) for Atlas
atlas_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# Create Atlas - The Discovery Agent
atlas = Agent(
    role="Travel Discovery Specialist",
    goal="Find the perfect travel destinations that match the user's mood, interests, and budget",
    backstory="""You are Atlas, an experienced world traveler and destination expert 
    with 15 years of experience exploring hidden gems around the globe. You have an 
    incredible talent for understanding what people are looking for in a trip - whether 
    it's adventure, relaxation, culture, or nature. You know the best times to visit, 
    budget-friendly options, and can find destinations that most people have never 
    heard of. You're passionate about helping people discover places that will create 
    unforgettable memories.
    
    IMPORTANT: You can ONLY use the 'Web Search' tool to find destinations.
    When searching, use queries like: 'best trekking destinations [region]',
    'budget travel [country]', 'adventure travel under $500'.
    Do NOT try to use any other tools.""",
    tools=[web_search_tool],
    llm=atlas_llm,
    verbose=True
)


if __name__ == "__main__":
    # Test Atlas
    print("=" * 60)
    print("🗺️  ATLAS - Travel Discovery Agent")
    print("=" * 60)
    print(f"Role: {atlas.role}")
    print(f"Goal: {atlas.goal}")
    print(f"Tools available: {len(atlas.tools)}")
    print("=" * 60)